import unittest
from tools.kubernetes_tools import get_pod_details, get_logs_for_pod

class TestKubernetesTools(unittest.TestCase):
    def test_get_pod_details(self):
        pod_details = get_pod_details("main-cluster", "frontend-pod-abc123", "default")
        expected_output = {
            "cluster_name": "main-cluster",
            "pod_name": "frontend-pod-abc123",
            "namespace": "default",
            "status": "Running",
            "restarts": 3,
            "age": "3d"
        }
        self.assertEqual(json.loads(pod_details.output), expected_output)

    def test_get_logs_for_pod(self):
        logs = get_logs_for_pod("main-cluster", "frontend-pod-abc123", "default")
        expected_logs = [
            "2024-06-10 10:00:00 Error: Out of memory",
            "2024-06-10 10:05:00 Restarting pod",
        ]
        self.assertEqual(json.loads(logs.output), expected_logs)

if __name__ == '__main__':
    unittest.main()
