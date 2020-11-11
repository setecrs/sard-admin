import unittest
from typing import List
import array
import requests
from kubernetes import client

from .k8s import _listWorkers, IPEDWorker, _getMetrics, MetricsException


class TestKubernetes(unittest.TestCase):
    def test_listEmptyIpedWorkers(self):
        pods = []
        podList = client.V1PodList(items=pods)
        workers: List[IPEDWorker] = _listWorkers(podList)
        self.assertListEqual(workers, [])

    def test_list1IpedWorker(self):
        state = client.V1ContainerState(running=None)
        containerStatus = client.V1ContainerStatus(
            image='image', image_id='1', name='2', ready=True, restart_count=0, state=state)
        status = client.V1PodStatus(
            host_ip="1.2.3.4", pod_ip='6.7.8.9', container_statuses=[containerStatus])
        metadata = client.V1ObjectMeta(name='ipedworker-myname')
        spec = client.V1PodSpec(node_name='sardcloudXX', containers=[])
        pods = [client.V1Pod(status=status, metadata=metadata, spec=spec)]
        podList = client.V1PodList(items=pods)
        workers: List[IPEDWorker] = _listWorkers(podList)
        self.assertEqual(len(workers), 1)
        w0: IPEDWorker = workers[0]
        self.assertEqual(w0.name, "ipedworker-myname")
        self.assertEqual(w0.host_ip, "1.2.3.4")
        self.assertEqual(w0.pod_ip, "6.7.8.9")
        self.assertEqual(w0.node_name, "sardcloudXX")
        self.assertEqual(w0.ready, True)
        self.assertEqual(w0.image, 'image')

    def test_filterIpedWorkers(self):
        status = client.V1PodStatus(host_ip="1.2.3.4", pod_ip='6.7.8.9')
        metadata = client.V1ObjectMeta(name='notipedworker-myname')
        spec = client.V1PodSpec(node_name='sardcloudXX', containers=[])
        pods = [client.V1Pod(status=status, metadata=metadata, spec=spec)]
        podList = client.V1PodList(items=pods)
        workers: List[IPEDWorker] = _listWorkers(podList)
        self.assertEqual(len(workers), 0)

    def test_Error_getMetrics(self):
        resp = requests.Response()
        resp.status_code = 500
        resp._content = b'testing'
        with self.assertRaises(MetricsException):
            _getMetrics(resp)

    def test_getMetrics_evidence(self):
        resp = requests.Response()
        resp.status_code = 200
        resp._content = b"""# HELP ipedworker_runIped_calls Number of calls to runIped
# TYPE ipedworker_runIped_calls counter
ipedworker_runIped_calls{evidence="/operacoes/operacao_teste/M160006/M160006.dd",hostname="ipedworker-ctlln"} 1
# HELP ipedworker_runIped_running Whether IPED is running or not
# TYPE ipedworker_runIped_running gauge
ipedworker_runIped_running{evidence="/operacoes/operacao_teste/M160006/M160006.dd",hostname="ipedworker-ctlln"} 1
"""
        mdata = _getMetrics(resp)
        self.assertEqual(mdata.evidence, "/operacoes/operacao_teste/M160006/M160006.dd")

    def test_getMetrics_progress(self):
        resp = requests.Response()
        resp.status_code = 200
        resp._content = b"""# HELP ipedworker_runIped_calls Number of calls to runIped
# TYPE ipedworker_runIped_calls counter
ipedworker_runIped_calls{evidence="/operacoes/2020.0010712/Equipe03/item04_M200234/item04_M200234.dd",hostname="ipedworker-hmcjt"} 1
# HELP ipedworker_runIped_found Number of items found
# TYPE ipedworker_runIped_found gauge
ipedworker_runIped_found{evidence="/operacoes/2020.0010712/Equipe03/item04_M200234/item04_M200234.dd",hostname="ipedworker-hmcjt"} 50903
# HELP ipedworker_runIped_processed Number of items processed
# TYPE ipedworker_runIped_processed gauge
ipedworker_runIped_processed{evidence="/operacoes/2020.0010712/Equipe03/item04_M200234/item04_M200234.dd",hostname="ipedworker-hmcjt"} 49091
# HELP ipedworker_runIped_running Whether IPED is running or not
# TYPE ipedworker_runIped_running gauge
ipedworker_runIped_running{evidence="/operacoes/2020.0010712/Equipe03/item04_M200234/item04_M200234.dd",hostname="ipedworker-hmcjt"} 1
"""
        mdata = _getMetrics(resp)
        self.assertEqual(mdata.processed, 49091)
        self.assertEqual(mdata.found, 50903)
