# --------------------------------------------------------------------------------------------
# Copyright (c) 2019 Virtustream Corporation.
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError
from azext_vmware.vendored_sdks.virtustream_client import VirtustreamClient

def privatecloud_list(cmd, client: VirtustreamClient, resource_group_name=None):
    if resource_group_name is not None:
        return client.private_cloud.list_in_resource_group(resource_group_name)
    else:
        return client.private_cloud.list()

def privatecloud_show(cmd, client: VirtustreamClient, resource_group_name, resource_name):
    return client.private_cloud.get_by_id_in_resource_group(resource_group_name, resource_name)

def privatecloud_create(cmd, client: VirtustreamClient, resource_group_name, resource_name, location, cluster_size, vpc, circuit_primary_subnet=None, circuit_secondary_subnet=None, tags=[]):
    from azext_vmware.vendored_sdks.models import AzurePrivateCloudRequest, PrivateCloud, Circuit, Cluster
    if circuit_primary_subnet is not None or circuit_secondary_subnet is not None:
        circuit = Circuit(primary_subnet=circuit_primary_subnet, secondary_subnet=circuit_secondary_subnet)
    else:
        circuit = None
    cluster = Cluster(cluster_size=cluster_size)
    properties = PrivateCloud(circuit=circuit, cluster=cluster, vpc=vpc)
    parameters = AzurePrivateCloudRequest(location=location, properties=properties, tags=tags)
    return client.private_cloud.create(resource_group_name, resource_name, parameters)

def privatecloud_delete(cmd, client: VirtustreamClient, resource_group_name, resource_name):
    return client.private_cloud.delete(resource_group_name, resource_name)

def privatecloud_modify(cmd, client: VirtustreamClient, resource_group_name, resource_name, location, circuit_primary_subnet=None, circuit_secondary_subnet=None, cluster_size=None, vpc=None, tags=[]):
    from azext_vmware.vendored_sdks.models import AzurePrivateCloudRequest, PrivateCloud, Circuit, Cluster
    circuit = Circuit(primary_subnet=circuit_primary_subnet, secondary_subnet=circuit_secondary_subnet)
    cluster = Cluster(cluster_size=cluster_size)
    properties = PrivateCloud(circuit=circuit, cluster=cluster, vpc=vpc)
    parameters = AzurePrivateCloudRequest(location=location, properties=properties, tags=tags)
    return client.private_cloud.modify(resource_group_name, resource_name, parameters)

def privatecloud_operationresults_show(cmd, client: VirtustreamClient, resource_group_name, resource_name, operation_id):
    return client.private_cloud.operation_results_get_by_id(resource_group_name=resource_group_name, private_cloud_name=resource_name, operation_id=operation_id)

def privatecloud_operationstatuses_show(cmd, client: VirtustreamClient, resource_group_name, resource_name, operation_id):
    return client.private_cloud.operation_statuses_get_by_id(resource_group_name=resource_group_name, private_cloud_name=resource_name, operation_id=operation_id)

def privatecloud_addauthorization(cmd, client: VirtustreamClient, resource_group_name, resource_name, authorization_name):
    return client.private_cloud.add_authorization(resource_group_name=resource_group_name, private_cloud_name=resource_name, authorization_name=authorization_name)

def privatecloud_deleteauthorization(cmd, client: VirtustreamClient, resource_group_name, resource_name, authorization_name):
    return client.private_cloud.delete_authorization(resource_group_name=resource_group_name, private_cloud_name=resource_name, authorization_name=authorization_name)

def privatecloud_addglobalreachconnection(cmd, client: VirtustreamClient, resource_group_name, resource_name, id, key):
    from azext_vmware.vendored_sdks.models import GlobalReachConnectionRequest, GlobalReachConnection
    parameters = GlobalReachConnectionRequest(id=id, key=key)
    return client.private_cloud.add_global_reach_connection(resource_group_name=resource_group_name, private_cloud_name=resource_name, parameters=parameters)

def privatecloud_deleteglobalreachconnection(cmd, client: VirtustreamClient, resource_group_name, resource_name, id):
    from azext_vmware.vendored_sdks.models import DeleteGlobalReachConnectionRequest
    parameters = DeleteGlobalReachConnectionRequest(id=id)
    return client.private_cloud.delete_global_reach_connection(resource_group_name=resource_group_name, private_cloud_name=resource_name, parameters=parameters)

def privatecloud_moveresources(cmd, client: VirtustreamClient, resource_group_name, resources, target_resource_group):
    from azext_vmware.vendored_sdks.models import MoveResourceRequest
    parameters = MoveResourceRequest(resources=resources, target_resource_group=target_resource_group)
    return client.private_cloud.move_resources(resource_group_name=resource_group_name, parameters=parameters)

def privatecloud_addidentitysource(cmd, client: VirtustreamClient, resource_group_name, resource_name, name, alias, domain, base_user_dn, base_group_dn, primary_server, secondary_server, use_ssl, username, credential):
    from azext_vmware.vendored_sdks.models import AddIdentitySourceRequest
    parameters = AddIdentitySourceRequest(name=name, alias=alias, domain=domain, base_user_dn=base_user_dn, base_group_dn=base_group_dn, primary_server=primary_server, secondary_server=secondary_server, use_ssl=use_ssl, username=username, credential=credential)
    return client.private_cloud.add_identity_source(resource_group_name=resource_group_name, private_cloud_name=resource_name, parameters=parameters)

def privatecloud_deleteidentitysource(cmd, client: VirtustreamClient, resource_group_name, resource_name, name, alias, domain):
    from azext_vmware.vendored_sdks.models import DeleteIdentitySourceRequest
    parameters = DeleteIdentitySourceRequest(name=name, alias=alias, domain=domain)
    return client.private_cloud.delete_identity_source(resource_group_name=resource_group_name, private_cloud_name=resource_name, parameters=parameters)

def privatecloud_getadmincredentials(cmd, client: VirtustreamClient, resource_group_name, resource_name):
    return client.private_cloud.get_admin_credentials(resource_group_name=resource_group_name, private_cloud_name=resource_name)

def cluster_create(cmd, client: VirtustreamClient, resource_group_name, location, resource_name, parent_resource_name, size, tags=[]):
    from azext_vmware.vendored_sdks.models import AzureClusterRequest, ClusterRequest
    properties = ClusterRequest(cluster_size=size)
    parameters = AzureClusterRequest(location=location, properties=properties, tags=tags)
    return client.cluster.create(resource_group_name=resource_group_name, private_cloud_name=parent_resource_name, cluster_name=resource_name, parameters=parameters)

def cluster_modify(cmd, client: VirtustreamClient, resource_group_name, location, resource_name, parent_resource_name, size, tags=[]):
    from azext_vmware.vendored_sdks.models import AzureClusterRequest, ClusterRequest
    properties = ClusterRequest(cluster_size=size)
    parameters = AzureClusterRequest(location=location, properties=properties, tags=tags)
    return client.cluster.modify(resource_group_name=resource_group_name, private_cloud_name=parent_resource_name, cluster_name=resource_name, parameters=parameters)

def cluster_list(cmd, client: VirtustreamClient, resource_group_name, parent_resource_name):
    return client.cluster.list(resource_group_name=resource_group_name, private_cloud_name=parent_resource_name)

def cluster_show(cmd, client: VirtustreamClient, resource_group_name, parent_resource_name, resource_name):
    return client.cluster.get_by_name(resource_group_name=resource_group_name, private_cloud_name=parent_resource_name, cluster_name=resource_name)

def cluster_delete(cmd, client: VirtustreamClient, resource_group_name, parent_resource_name, resource_name):
    return client.cluster.delete(resource_group_name=resource_group_name, private_cloud_name=parent_resource_name, cluster_name=resource_name)