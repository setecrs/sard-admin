from typing import List
from collections import namedtuple
from kubernetes import client, config
import requests
from prometheus_client.parser import text_string_to_metric_families

IPEDWorker = namedtuple('IPEDWorker', [
    'name',
    'pod_ip',
    'host_ip',
    'node_name',
    'ready',
    'image'
])

class K8s:
    def __init__(self, namespace="default"):
        self.namespace=namespace
        config.load_kube_config()
    def listWorkers(self) -> List[IPEDWorker]:
        resp = client.CoreV1Api().list_namespaced_pod(self.namespace)
        return _listWorkers(resp)

def getEvidence(pod_ip, pod_port=80) -> str:
    resp = requests.get(f"http://{pod_ip}:{pod_port}/metrics")
    return _getEvidence(resp)

class MetricsException(Exception):
    pass

def _getEvidence(resp:requests.Response) -> str:
    if (not resp.ok):
        raise MetricsException("Could not get metrics: "+ resp.text)
    for family in text_string_to_metric_families(resp.text):
        for sample in family.samples:
            if sample.name=='ipedworker_runIped_running':
                return sample.labels['evidence']
    return ''

def _listWorkers(resp:client.V1PodList) -> List[IPEDWorker]:
    result:List[IPEDWorker] = []
    item = client.V1Pod()
    for item in resp.items:
        name = item.metadata.name
        if not name.startswith('ipedworker'):
            continue
        status:client.V1PodStatus = item.status
        pod_ip = status.pod_ip
        host_ip = status.host_ip
        node_name = item.spec.node_name
        ready = False
        image = ''
        if len(status.container_statuses) == 1:
            container_status:client.V1ContainerStatus = status.container_statuses[0]
            ready = container_status.ready
            image = container_status.image
        worker = IPEDWorker(
            name=name,
            host_ip=host_ip,
            pod_ip=pod_ip,
            node_name=node_name,
            ready=ready,
            image=image,
        )
        result.append(worker)
    return result

