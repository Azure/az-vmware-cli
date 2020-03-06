# --------------------------------------------------------------------------------------------
# Copyright (c) 2019 Virtustream Corporation.
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError
from azext_vmware.vendored_sdks.virtustream_client import VirtustreamClient

def privatecloud_list(cmd, client: VirtustreamClient, resource_group_name=None):
    if resource_group_name is None:
        return client.private_clouds.list_in_subscription()
    else:
        return client.private_clouds.list(resource_group_name)

def privatecloud_show(cmd, client: VirtustreamClient, resource_group_name, name):
    return client.private_clouds.get(resource_group_name, name)

def privatecloud_create(cmd, client: VirtustreamClient, resource_group_name, name, location, sku, cluster_size, network_block, circuit_primary_subnet=None, circuit_secondary_subnet=None, internet=None, vcenter_password=None, nsxt_password=None, tags=[]):
    from azext_vmware.vendored_sdks.models import PrivateCloud, PrivateCloudProperties, Circuit, DefaultClusterProperties, Sku
    if circuit_primary_subnet is not None or circuit_secondary_subnet is not None:
        circuit = Circuit(primary_subnet=circuit_primary_subnet, secondary_subnet=circuit_secondary_subnet)
    else:
        circuit = None
    clusterProps = DefaultClusterProperties(cluster_size=cluster_size)
    cloudProps = PrivateCloudProperties(circuit=circuit, cluster=clusterProps, network_block=network_block)
    cloud = PrivateCloud(location=location, sku=Sku(name=sku), properties=cloudProps, tags=tags)
    if internet is not None:
        cloud.properties.internet = internet
    if vcenter_password is not None:
        cloud.properties.vcenter_password = vcenter_password
    if nsxt_password is not None:
        cloud.properties.nsxt_password = nsxt_password
    return client.private_clouds.create_or_update(resource_group_name, name, cloud)

def privatecloud_update(cmd, client: VirtustreamClient, resource_group_name, name, cluster_size=None, internet=None):
    cloud = privatecloud_show(cmd, client, resource_group_name, name)
    if cluster_size is not None:
        cloud.properties.cluster.cluster_size = cluster_size
    if internet is not None:
        cloud.properties.internet = internet
    return client.private_clouds.update(resource_group_name, name, cloud)

def privatecloud_delete(cmd, client: VirtustreamClient, resource_group_name, name):
    return client.private_clouds.delete(resource_group_name, name)

def privatecloud_listadmincredentials(cmd, client: VirtustreamClient, resource_group_name, private_cloud):
    return client.private_clouds.list_admin_credentials(resource_group_name=resource_group_name, private_cloud_name=private_cloud)

def privatecloud_addidentitysource(cmd, client: VirtustreamClient, resource_group_name, name, private_cloud, alias, domain, base_user_dn, base_group_dn, primary_server, secondary_server, ssl, username, password):
    from azext_vmware.vendored_sdks.models import IdentitySource
    pc = client.private_clouds.get(resource_group_name, private_cloud)
    identitysource = IdentitySource(name=name, alias=alias, domain=domain, base_user_dn=base_user_dn, base_group_dn=base_group_dn, primary_server=primary_server, secondary_server=secondary_server, ssl=ssl, username=username, password=password)
    pc.properties.identity_sources.append(identitysource)
    return client.private_clouds.update(resource_group_name=resource_group_name, private_cloud_name=private_cloud, private_cloud=pc)

def privatecloud_deleteidentitysource(cmd, client: VirtustreamClient, resource_group_name, name, private_cloud, alias, domain):
    from azext_vmware.vendored_sdks.models import IdentitySource
    pc = client.private_clouds.get(resource_group_name, private_cloud)
    found = next((ids for ids in pc.properties.identity_sources 
        if ids.name == name and ids.alias == alias and ids.domain == domain), None)
    if found:
        pc.properties.identity_sources.remove(found)
        return client.private_clouds.update(resource_group_name=resource_group_name, private_cloud_name=private_cloud, private_cloud=pc)
    else:
        return pc

def privatecloud_addauthorization(cmd, client: VirtustreamClient, resource_group_name, private_cloud, name):
    from azext_vmware.vendored_sdks.models import ExpressRouteAuthorization
    pc = client.private_clouds.get(resource_group_name, private_cloud)
    auth = ExpressRouteAuthorization(name=name)
    pc.properties.circuit.authorizations.append(auth)
    return client.private_clouds.update(resource_group_name=resource_group_name, private_cloud_name=private_cloud, private_cloud=pc)

def privatecloud_deleteauthorization(cmd, client: VirtustreamClient, resource_group_name, private_cloud, name):
    from azext_vmware.vendored_sdks.models import ExpressRouteAuthorization
    pc = client.private_clouds.get(resource_group_name, private_cloud)
    found = next((auth for auth in pc.properties.circuit.authorizations
        if auth.name == name), None)
    if found:
        pc.properties.circuit.authorizations.remove(found)
        return client.private_clouds.update(resource_group_name=resource_group_name, private_cloud_name=private_cloud, private_cloud=pc)
    else:
        return pc

def cluster_create(cmd, client: VirtustreamClient, resource_group_name, location, name, private_cloud, size, tags=[]):
    from azext_vmware.vendored_sdks.models import Cluster, ClusterProperties
    clusterProps = ClusterProperties(cluster_size=size)
    cluster = Cluster(location=location, properties=clusterProps, tags=tags)
    return client.clusters.create_or_update(resource_group_name=resource_group_name, private_cloud_name=private_cloud, cluster_name=name, cluster=cluster)

def cluster_update(cmd, client: VirtustreamClient, resource_group_name, location, name, private_cloud, size, tags=[]):
    from azext_vmware.vendored_sdks.models import Cluster, ClusterProperties
    clusterProps = ClusterProperties(cluster_size=size)
    cluster = Cluster(location=location, properties=clusterProps, tags=tags)
    return client.clusters.update(resource_group_name=resource_group_name, private_cloud_name=private_cloud, cluster_name=name, cluster=cluster)

def cluster_list(cmd, client: VirtustreamClient, resource_group_name, private_cloud):
    return client.clusters.list(resource_group_name=resource_group_name, private_cloud_name=private_cloud)

def cluster_show(cmd, client: VirtustreamClient, resource_group_name, private_cloud, name):
    return client.clusters.get(resource_group_name=resource_group_name, private_cloud_name=private_cloud, cluster_name=name)

def cluster_delete(cmd, client: VirtustreamClient, resource_group_name, private_cloud, name):
    return client.clusters.delete(resource_group_name=resource_group_name, private_cloud_name=private_cloud, cluster_name=name)