# --------------------------------------------------------------------------------------------
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
            'loc': 'northcentralus',
            'privatecloud': 'cloud1',
            'cluster': 'cluster1'
        })

        # show should throw ResourceNotFound
        with self.assertRaisesRegexp(ApiErrorException, 'ResourceNotFound'):
            self.cmd('vmware private-cloud show -g {rg} -n {privatecloud}')

        count = len(self.cmd('vmware private-cloud list -g {rg}').get_output_in_json())
        self.assertEqual(count, 0, 'private cloud count expected to be 0')

        # create a private cloud
        self.cmd('vmware private-cloud create -g {rg} -n {privatecloud} --location {loc} --sku he --cluster-size 4 --network-block 192.168.48.0/22 --nsxt-password 5rqdLj4GF3cePUe6( --vcenter-password UpfBXae9ZquZSDXk( ')

        count = len(self.cmd('vmware private-cloud list -g {rg}').get_output_in_json())
        self.assertEqual(count, 1, 'private cloud count expected to be 1')

        # count at the subscription level
        # test passes, but commented out for privacy
        # count = len(self.cmd('vmware private-cloud list').get_output_in_json())
        # self.assertGreaterEqual(count, 1, 'subscription private cloud count expected to be more than 1')

        # poll until it is no longer ResourceNotFound
        await self.poll_until_no_exception(lambda: self.cmd('vmware private-cloud show -g {rg} -n {privatecloud}'), ApiErrorException)
        await self.poll_until_result(lambda: self.cmd('vmware private-cloud show -g {rg} -n {privatecloud}'), provissioning_succeeded)

        # get admin credentials
        # TODO VCFM-2605 not currently supported in test environment
        # self.cmd('vmware private-cloud listadmincredentials -g {rg} -n {privatecloud}')

        # update private cloud to changed default cluster size
        self.cmd('vmware private-cloud update -g {rg} -n {privatecloud} --cluster-size 3')

        # update private cloud to enable internet
        self.cmd('vmware private-cloud update -g {rg} -n {privatecloud} --internet enabled')

        # add authorization
        self.cmd('vmware private-cloud addauthorization -g {rg} -c {privatecloud} -n myauthname')
        await self.poll_until_result(lambda: self.cmd('vmware private-cloud show -g {rg} -n {privatecloud}'), provissioning_succeeded)

        # delete authorization
        self.cmd('vmware private-cloud deleteauthorization -g {rg} -c {privatecloud} -n myauthname')
        await self.poll_until_result(lambda: self.cmd('vmware private-cloud show -g {rg} -n {privatecloud}'), provissioning_succeeded)

        # add identity source
        self.cmd('vmware private-cloud addidentitysource -g {rg} -c {privatecloud} -n groupName --alias groupAlias --domain domain --base-user-dn "ou=baseUser" --base-group-dn "ou=baseGroup" --primary-server ldaps://1.1.1.1:636 --username someone --password something')
        await self.poll_until_result(lambda: self.cmd('vmware private-cloud show -g {rg} -n {privatecloud}'), provissioning_succeeded)

        # delete identity source
        self.cmd('vmware private-cloud deleteidentitysource -g {rg} -c {privatecloud} -n groupName --alias groupAlias --domain domain')
        await self.poll_until_result(lambda: self.cmd('vmware private-cloud show -g {rg} -n {privatecloud}'), provissioning_succeeded)

        # cluster list should report 0
        count = len(self.cmd('vmware cluster list -g {rg} -c {privatecloud}').get_output_in_json())
        self.assertEqual(count, 0, 'cluster count expected to be 0')

        # cluster create
        self.cmd('vmware cluster create -g {rg} -c {privatecloud} -n {cluster} --size 3')
        await self.poll_until_result(lambda: self.cmd('vmware cluster show -g {rg} -c {privatecloud} -n {cluster}'), provissioning_succeeded)

        # cluster list should report 1
        count = len(self.cmd('vmware cluster list -g {rg} -c {privatecloud}').get_output_in_json())
        self.assertEqual(count, 1, 'cluster count expected to be 1')

        # cluster update
        self.cmd('vmware cluster update -g {rg} -c {privatecloud} -n {cluster} --size 4')
        await self.poll_until_result(lambda: self.cmd('vmware cluster show -g {rg} -c {privatecloud} -n {cluster}'), provissioning_succeeded)

        # cluster delete
        self.cmd('vmware cluster delete -g {rg} -c {privatecloud} -n {cluster}')
        await self.poll_until_result(lambda: self.cmd('vmware private-cloud show -g {rg} -n {privatecloud}'), provissioning_succeeded)

        # delete the private cloud
        self.cmd('vmware private-cloud delete -g {rg} -n {privatecloud}')

        count = len(self.cmd('vmware private-cloud list -g {rg}').get_output_in_json())
        self.assertEqual(count, 0, 'private cloud count expected to be 0')

        # it should throw ResourceNotFound
        await self.poll_until_exception(lambda: self.cmd('vmware private-cloud show -g {rg} -n {privatecloud}'), ApiErrorException)