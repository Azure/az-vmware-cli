# --------------------------------------------------------------------------------------------
# Copyright (c) 2019 Virtustream Corporation.
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError
from azext_vmware.vendored_sdks.virtustream_client import VirtustreamClient

def privatecloud_list(cmd, client: VirtustreamClient, resource_group_name):
    return client.private_clouds.list(resource_group_name)

def privatecloud_show(cmd, client: VirtustreamClient, resource_group_name, resource_name):
    return client.private_clouds.get(resource_group_name, resource_name)

def privatecloud_create(cmd, client: VirtustreamClient, resource_group_name, resource_name, location, cluster_size, network_block, circuit_primary_subnet=None, circuit_secondary_subnet=None, tags=[]):
    from azext_vmware.vendored_sdks.models import PrivateCloud, PrivateCloudProperties, Circuit, DefaultClusterProperties
    if circuit_primary_subnet is not None or circuit_secondary_subnet is not None:
        circuit = Circuit(primary_subnet=circuit_primary_subnet, secondary_subnet=circuit_secondary_subnet)
    else:
        circuit = None
    clusterProps = DefaultClusterProperties(cluster_size=cluster_size)
    cloudProps = PrivateCloudProperties(circuit=circuit, cluster=clusterProps, network_block=network_block)
    cloud = PrivateCloud(location=location, properties=cloudProps, tags=tags)
    return client.private_clouds.create_or_update(resource_group_name, resource_name, cloud)

def privatecloud_delete(cmd, client: VirtustreamClient, resource_group_name, resource_name):
    return client.private_clouds.delete(resource_group_name, resource_name)

def privatecloud_listadmincredentials(cmd, client: VirtustreamClient, resource_group_name, resource_name):
    return client.private_clouds.list_admin_credentials(resource_group_name=resource_group_name, private_cloud_name=resource_name)


def cluster_create(cmd, client: VirtustreamClient, resource_group_name, location, resource_name, parent_resource_name, size, tags=[]):
    from azext_vmware.vendored_sdks.models import Cluster, ClusterProperties
    clusterProps = ClusterProperties(cluster_size=size)
    cluster = Cluster(location=location, properties=clusterProps, tags=tags)
    return client.clusters.create_or_update(resource_group_name=resource_group_name, private_cloud_name=parent_resource_name, cluster_name=resource_name, cluster=cluster)

def cluster_update(cmd, client: VirtustreamClient, resource_group_name, location, resource_name, parent_resource_name, size, tags=[]):
    from azext_vmware.vendored_sdks.models import Cluster, ClusterProperties
    clusterProps = ClusterProperties(cluster_size=size)
    cluster = Cluster(location=location, properties=clusterProps, tags=tags)
    return client.clusters.update(resource_group_name=resource_group_name, private_cloud_name=parent_resource_name, cluster_name=resource_name, cluster=cluster)

def cluster_list(cmd, client: VirtustreamClient, resource_group_name, parent_resource_name):
    return client.clusters.list(resource_group_name=resource_group_name, private_cloud_name=parent_resource_name)

def cluster_show(cmd, client: VirtustreamClient, resource_group_name, parent_resource_name, resource_name):
    return client.clusters.get(resource_group_name=resource_group_name, private_cloud_name=parent_resource_name, cluster_name=resource_name)

def cluster_delete(cmd, client: VirtustreamClient, resource_group_name, parent_resource_name, resource_name):
    return client.clusters.delete(resource_group_name=resource_group_name, private_cloud_name=parent_resource_name, cluster_name=resource_name)