# --------------------------------------------------------------------------------------------
# Copyright (c) 2019 Virtustream Corporation.
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.commands import CliCommandType
from azext_vmware._client_factory import cf_vmware

def load_command_table(self, _):

    vmware_sdk = CliCommandType(
        operations_tmpl='azext_vmware.vendored_sdks.operations#PrivateCloudOperations.{}',
        client_factory=cf_vmware)

    with self.command_group('vmware privatecloud', vmware_sdk, client_factory=cf_vmware) as g:
        g.custom_command('list', 'privatecloud_list')
        g.custom_command('show', 'privatecloud_show')
        g.custom_command('create', 'privatecloud_create')
        # g.custom_command('modify', 'privatecloud_modify')
        g.custom_command('delete', 'privatecloud_delete')
        g.custom_command('addauthorization', 'privatecloud_addauthorization')
        g.custom_command('deleteauthorization', 'privatecloud_deleteauthorization')
        g.custom_command('addglobalreachconnection', 'privatecloud_addglobalreachconnection')
        g.custom_command('deleteglobalreachconnection', 'privatecloud_deleteglobalreachconnection')
        g.custom_command('addidentitysource', 'privatecloud_addidentitysource')
        g.custom_command('deleteidentitysource', 'privatecloud_deleteidentitysource')
        g.custom_command('getadmincredentials', 'privatecloud_getadmincredentials')

    # with self.command_group('vmware privatecloud operationresults', vmware_sdk, client_factory=cf_vmware) as g:
    #     g.custom_command('show', 'privatecloud_operationresults_show')

    # with self.command_group('vmware privatecloud operationstatuses', vmware_sdk, client_factory=cf_vmware) as g:
    #     g.custom_command('show', 'privatecloud_operationstatuses_show')

    with self.command_group('vmware cluster', vmware_sdk, client_factory=cf_vmware) as g:
        g.custom_command('create', 'cluster_create')
        g.custom_command('modify', 'cluster_modify')
        g.custom_command('list', 'cluster_list')
        g.custom_command('delete', 'cluster_delete')
        g.custom_command('show', 'cluster_show')