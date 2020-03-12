#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) 2019 Virtustream Corporation.
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from codecs import open
from setuptools import setup, find_packages
# try:
#     from azure_bdist_wheel import cmdclass
# except ImportError:
#     from distutils import log as logger
#     logger.warn("Wheel is not available, disabling bdist_wheel hook")

VERSION = "0.5.3"

# TODO: Add any additional SDK dependencies here
DEPENDENCIES = [
    # 'azure-cli-core'
]

setup(
    name='vmware',
    version=VERSION,
    description='Preview Azure VMware Solution by Virtustream commands.',
    long_description='Additional commands providing support for preview Azure VMware Solution by Virtustream features.',
    license='MIT',
    author='Virtustream',
    author_email='azpycli@virtustream.com',
    url='https://github.com/virtustream/azure-vmware-virtustream-cli-extension',
    packages=find_packages(exclude=["tests"]),
    install_requires=DEPENDENCIES,
    package_data={'azext_vmware': ['azext_metadata.json']}
)