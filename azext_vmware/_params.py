# --------------------------------------------------------------------------------------------
# Copyright (c) 2019 Virtustream Corporation.
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long

def load_arguments(self, _):

    from azure.cli.core.commands.parameters import tags_type
    from azure.cli.core.commands.validators import get_default_location_from_resource_group

    with self.argument_context('vmware') as c:
        c.argument('resource_name', options_list=['--resource-name', '-n'], help='Name of the resource.')
        c.argument('tags', tags_type)
        c.argument('location', validator=get_default_location_from_resource_group)

    with self.argument_context('vmware privatecloud') as c:
        c.argument('circuit_primary_subnet', help='A /30 subnet for the primary circuit in the Express Route to configure routing between your network and Microsoft\'s Enterprise edge (MSEEs) routers.')
        c.argument('circuit_secondary_subnet', help='A /30 subnet for the secondary circuit in the Express Route to configure routing between your network and Microsoft\'s Enterprise edge (MSEEs) routers.')
        c.argument('cluster_size', help='Number of hosts for the new cluster. Minimum 4, Maximum 16.')
        c.argument('network_block', help='A subnet at least of size /22.')

    with self.argument_context('vmware cluster') as c:
        c.argument('parent_resource_name', options_list=['--parent-resource-name', '-p'], help='Name of the parent resource, the name of the private cloud.')
        c.argument('size', help='Number of hosts for the new cluster.')
