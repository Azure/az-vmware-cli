# --------------------------------------------------------------------------------------------
# Copyright (c) 2019 Virtustream Corporation.
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import unittest
import asyncio
import functools

from azure_devtools.scenario_tests import AllowLargeResponse
from azure.cli.testsdk import (ScenarioTest, ResourceGroupPreparer)
from azext_vmware.vendored_sdks.models import ApiErrorException

class AsyncScenarioTest(ScenarioTest):

    @staticmethod
    def await_prepared_test(test_fn):
        """Synchronous wrapper for async test methods. Used to avoid making changes
        upstream to AbstractPreparer (which doesn't await the functions it wraps)
        """

        @functools.wraps(test_fn)
        def run(test_class_instance, *args, **kwargs):
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(test_fn(test_class_instance))

        return run

    async def poll_until_no_exception(self, fn, expected_exception, max_retries=20, retry_delay=3):
        """polling helper for live tests because some operations take an unpredictable amount of time to complete"""

        for i in range(max_retries):
            try:
                fn()
                break
            except expected_exception:
                print("caught %d").format(i)
                if i == max_retries - 1:
                    raise
                if self.is_live:
                    await asyncio.sleep(retry_delay)

    async def poll_until_exception(self, fn, expected_exception, max_retries=20, retry_delay=3):
        """polling helper for live tests because some operations take an unpredictable amount of time to complete"""

        for _ in range(max_retries):
            try:
                fn()
                if self.is_live:
                    await asyncio.sleep(retry_delay)
            except expected_exception:
                return
        self.fail("expected exception {expected_exception} was not raised")

    async def poll_until_result(self, cmd, check_result, max_retries=40, retry_delay=3):
        for _ in range(max_retries):
            rslt = cmd()
            if(check_result(rslt)):
                return
            if self.is_live:
                await asyncio.sleep(retry_delay)
        self.fail("expected result did not happen")

# Check if a privatecloud operation has succeeded.
# On create, the state switches from 'Building' to 'Succeeded'.
# On add and delete authorization from 'updating' to 'Succeeded'.
def provissioning_succeeded(rslt):
    state = rslt.get_output_in_json()['properties']['provisioningState']
    # print(state)
    return state == 'Succeeded'

class VmwareScenarioTest(AsyncScenarioTest):

    @ResourceGroupPreparer(name_prefix='cli_test_vmware')
    @AsyncScenarioTest.await_prepared_test
    async def test_vmware(self):
        self.kwargs.update({
            'loc': 'eastus2',
            'privatecloud': 'cloud1',
            'cluster': 'cluster1'
        })

        # show should throw ResourceNotFound
        with self.assertRaisesRegexp(ApiErrorException, 'ResourceNotFound'):
            self.cmd('vmware privatecloud show -g {rg} -n {privatecloud}')

        count = len(self.cmd('vmware privatecloud list -g {rg}').get_output_in_json())
        self.assertEqual(count, 0, 'private cloud count expected to be 0')

        # begin creating a private cloud
        self.cmd('vmware privatecloud create -g {rg} -n {privatecloud} --location {loc} --cluster-size 4 --network-block 192.168.48.0/22')

        count = len(self.cmd('vmware privatecloud list -g {rg}').get_output_in_json())
        self.assertEqual(count, 1, 'private cloud count expected to be 1')

        # poll until it is no longer ResourceNotFound
        await self.poll_until_no_exception(lambda: self.cmd('vmware privatecloud show -g {rg} -n {privatecloud}'), ApiErrorException)
        await self.poll_until_result(lambda: self.cmd('vmware privatecloud show -g {rg} -n {privatecloud}'), provissioning_succeeded)

        # get admin credentials
        self.cmd('vmware privatecloud listadmincredentials -g {rg} -n {privatecloud}')

        # add authorization
        self.cmd('vmware privatecloud addauthorization -g {rg} -n {privatecloud} --authorization-name myauthname')
        await self.poll_until_result(lambda: self.cmd('vmware privatecloud show -g {rg} -n {privatecloud}'), provissioning_succeeded)

        # delete authorization
        self.cmd('vmware privatecloud deleteauthorization -g {rg} -n {privatecloud} --authorization-name myauthname')
        await self.poll_until_result(lambda: self.cmd('vmware privatecloud show -g {rg} -n {privatecloud}'), provissioning_succeeded)

        # add identity source
        self.cmd('vmware privatecloud addidentitysource -g {rg} -n {privatecloud} --name groupName --alias groupAlias --domain domain --base-user-dn "ou=baseUser" --base-group-dn "ou=baseGroup" --primary-server ldaps://1.1.1.1:636 --secondary-server ldaps://1.1.1.2:636 --ssl Enabled --username someone --password something')
        await self.poll_until_result(lambda: self.cmd('vmware privatecloud show -g {rg} -n {privatecloud}'), provissioning_succeeded)

        # delete identity source
        self.cmd('vmware privatecloud deleteidentitysource -g {rg} -n {privatecloud} --name groupName --alias groupAlias --domain domain')
        await self.poll_until_result(lambda: self.cmd('vmware privatecloud show -g {rg} -n {privatecloud}'), provissioning_succeeded)

        # cluster list should report 0
        count = len(self.cmd('vmware cluster list -g {rg} -p {privatecloud}').get_output_in_json())
        self.assertEqual(count, 0, 'cluster count expected to be 0')

        # cluster create
        self.cmd('vmware cluster create -g {rg} -p {privatecloud} -n {cluster} --size 3 --location eastus')
        await self.poll_until_result(lambda: self.cmd('vmware cluster show -g {rg} -p {privatecloud} -n {cluster}'), provissioning_succeeded)

        # cluster list should report 1
        count = len(self.cmd('vmware cluster list -g {rg} -p {privatecloud}').get_output_in_json())
        self.assertEqual(count, 1, 'cluster count expected to be 1')

        # cluster update
        self.cmd('vmware cluster update -g {rg} --location {loc} -p {privatecloud} -n {cluster} --size 4')
        await self.poll_until_result(lambda: self.cmd('vmware cluster show -g {rg} -p {privatecloud} -n {cluster}'), provissioning_succeeded)

        # cluster delete
        self.cmd('vmware cluster delete -g {rg} -p {privatecloud} -n {cluster}')
        await self.poll_until_result(lambda: self.cmd('vmware privatecloud show -g {rg} -n {privatecloud}'), provissioning_succeeded)

        # delete the private cloud
        self.cmd('vmware privatecloud delete -g {rg} -n {privatecloud}')

        count = len(self.cmd('vmware privatecloud list -g {rg}').get_output_in_json())
        self.assertEqual(count, 0, 'private cloud count expected to be 0')

        # it should throw ResourceNotFound
        await self.poll_until_exception(lambda: self.cmd('vmware privatecloud show -g {rg} -n {privatecloud}'), ApiErrorException)