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

helps['vmware create'] = """
    type: command
    short-summary: Create a private cloud.
"""

helps['vmware list'] = """
    type: command
    short-summary: List private clouds.
"""

helps['vmware delete'] = """
    type: command
    short-summary: Delete a private cloud.
"""

helps['vmware show'] = """
    type: command
    short-summary: Show details of a private cloud.
"""

helps['vmware update'] = """
    type: command
    short-summary: Update a private cloud.
"""
