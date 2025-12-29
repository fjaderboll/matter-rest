from typing import Iterable

from app.models.schemas import AttributeInfo, ClusterInfo, EndpointInfo

def create_attribute_path(endpoint_id: int, cluster_id: int, attribute_id: int) -> str:
    return f"{endpoint_id}/{cluster_id}/{attribute_id}"

def map_attributes_to_objects(node: dict) -> dict:
    attributes = node.get("attributes") or {}
    endpoints = {}
    if isinstance(attributes, dict):
        for key in attributes.keys():
            parts = key.split("/")
            if len(parts) != 3:
                continue
            
            endpoint_id, cluster_id, attribute_id = map(int, parts)
            if endpoint_id in endpoints:
                endpoint = endpoints[endpoint_id]
            else:
                endpoint = EndpointInfo(id=endpoint_id, clusters={})
                endpoints[endpoint_id] = endpoint
            
            if cluster_id in endpoint.clusters:
                cluster = endpoint.clusters[cluster_id]
            else:
                cluster = ClusterInfo(id=cluster_id, attributes={})
                endpoint.clusters[cluster_id] = cluster
            
            attribute_info = create_attribute_info(endpoint_id, cluster_id, attribute_id, attributes[key])
            cluster.attributes[attribute_id] = attribute_info
            
        print(endpoints)
    return endpoints

def create_attribute_info(endpoint_id: int, cluster_id: int, attribute_id: int, value: any) -> AttributeInfo:
    attribute_path = create_attribute_path(endpoint_id, cluster_id, attribute_id)
    return AttributeInfo(id=attribute_id, path=attribute_path, value=value)