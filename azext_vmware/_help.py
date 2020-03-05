# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) 2019 Virtustream Corporation.
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.help_files import helps  # pylint: disable=unused-import


helps['vmware'] = """
    type: group
    short-summary: Commands to manage private clouds.
"""

helps['vmware private-cloud'] = """
    type: group
    short-summary: Commands to manage private clouds.
"""

helps['vmware cluster'] = """
    type: group
    short-summary: Commands to manage clusters in a private cloud.
"""

helps['vmware cluster create'] = """
    type: command
    short-summary: Create a cluster in a private cloud.
"""

helps['vmware cluster delete'] = """
    type: command
    short-summary: Delete a cluster in a private cloud.
"""

helps['vmware cluster list'] = """
    type: command
    short-summary: List clusters in a private cloud.
"""

helps['vmware cluster show'] = """
    type: command
    short-summary: Show details of a cluster in a private cloud.
"""

helps['vmware cluster update'] = """
    type: command
    short-summary: Update a cluster in a private cloud.
"""

helps['vmware private-cloud addauthorization'] = """
    type: command
    short-summary: Add an authorization to the ExpressRoute for a private cloud.
"""

helps['vmware private-cloud addidentitysource'] = """
    type: command
    short-summary: Add a vCenter Single Sign On Identity Source to a private cloud.
"""

helps['vmware private-cloud create'] = """
    type: command
    short-summary: Create a private cloud.
"""

helps['vmware private-cloud delete'] = """
    type: command
    short-summary: Delete a private cloud.
"""

helps['vmware private-cloud deleteauthorization'] = """
    type: command
    short-summary: Delete an authorization to the ExpressRoute for a private cloud.
"""

helps['vmware private-cloud deleteidentitysource'] = """
    type: command
    short-summary: Delete a vCenter Single Sign On Identity Source for a private cloud.
"""

helps['vmware private-cloud list'] = """
    type: command
    short-summary: List the private clouds.
"""

helps['vmware private-cloud listadmincredentials'] = """
    type: command
    short-summary: List the admin credentials for the private cloud.
"""

helps['vmware private-cloud show'] = """
    type: command
    short-summary: Show details of a private cloud.
"""

helps['vmware private-cloud update'] = """
    type: command
    short-summary: Update a private cloud.
"""