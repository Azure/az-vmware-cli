#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) 2019 Virtustream Corporation.
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from codecs import open
from setuptools import setup, find_packages

VERSION = "0.6.0"

DEPENDENCIES = [
]

setup(
    name='vmware',
    version=VERSION,
    description='Preview Azure VMware Solution commands.',
    long_description='Additional commands providing support for preview Azure VMware Solution features.',
    license='MIT',
    author='Microsoft',
    author_email='azpycli@microsoft.com',
    url='https://github.com/virtustream/azure-vmware-virtustream-cli-extension',
    packages=find_packages(exclude=["tests"]),
    install_requires=DEPENDENCIES,
    package_data={'azext_vmware': ['azext_metadata.json']}
)