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

def privatecloud_addidentitysource(cmd, client: VirtustreamClient, resource_group_name, resource_name, name, alias, domain, base_user_dn, base_group_dn, primary_server, secondary_server, ssl, username, password):
    from azext_vmware.vendored_sdks.models import IdentitySource
    privatecloud = client.private_clouds.get(resource_group_name, resource_name)
    identitysource = IdentitySource(name=name, alias=alias, domain=domain, base_user_dn=base_user_dn, base_group_dn=base_group_dn, primary_server=primary_server, secondary_server=secondary_server, ssl=ssl, username=username, password=password)
    privatecloud.properties.identity_sources.append(identitysource)
    return client.private_clouds.update(resource_group_name=resource_group_name, private_cloud_name=resource_name, private_cloud=privatecloud)

def privatecloud_deleteidentitysource(cmd, client: VirtustreamClient, resource_group_name, resource_name, name, alias, domain):
    from azext_vmware.vendored_sdks.models import IdentitySource
    privatecloud = client.private_clouds.get(resource_group_name, resource_name)
    found = next((ids for ids in privatecloud.properties.identity_sources 
        if ids.name == name and ids.alias == alias and ids.domain == domain), None)
    if found:
        privatecloud.properties.identity_sources.remove(found)
        return client.private_clouds.update(resource_group_name=resource_group_name, private_cloud_name=resource_name, private_cloud=privatecloud)
    else:
        return privatecloud

def privatecloud_addauthorization(cmd, client: VirtustreamClient, resource_group_name, resource_name, authorization_name):
    from azext_vmware.vendored_sdks.models import ExpressRouteAuthorization
    privatecloud = client.private_clouds.get(resource_group_name, resource_name)
    auth = ExpressRouteAuthorization(name=authorization_name)
    privatecloud.properties.circuit.authorizations.append(auth)
    return client.private_clouds.update(resource_group_name=resource_group_name, private_cloud_name=resource_name, private_cloud=privatecloud)

def privatecloud_deleteauthorization(cmd, client: VirtustreamClient, resource_group_name, resource_name, authorization_name):
    from azext_vmware.vendored_sdks.models import ExpressRouteAuthorization
    privatecloud = client.private_clouds.get(resource_group_name, resource_name)
    found = next((auth for auth in privatecloud.properties.circuit.authorizations
        if auth.name == authorization_name), None)
    if found:
        privatecloud.properties.circuit.authorizations.remove(found)
        return client.private_clouds.update(resource_group_name=resource_group_name, private_cloud_name=resource_name, private_cloud=privatecloud)
    else:
        return privatecloud

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