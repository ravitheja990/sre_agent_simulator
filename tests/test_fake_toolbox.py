import unittest
from fake_toolbox import FakeToolbox

class TestFakeToolbox(unittest.TestCase):

    def setUp(self):
        self.scenario = {
            "cluster_name": "test-cluster",
            "namespace": "default",
            "pods": [
                {
                    "name": "test-pod",
                    "status": "Running",
                    "restarts": 1,
                    "age": "2d"
                }
            ],
            "logs": [
                {
                    "name": "test-log",
                    "content": "Test log content"
                }
            ]
        }
        self.toolbox = FakeToolbox(self.scenario)

    def test_get_pod_details(self):
        pod_details = self.toolbox.get_tool("get_pod_details")(
            "test-cluster", "test-pod", "default")
        self.assertIsInstance(pod_details.output, str)

    def test_get_logs_for_pod(self):
        logs = self.toolbox.get_tool("get_logs_for_pod")(
            "test-cluster", "test-pod", "default")
        self.assertIsInstance(logs.output, str)

if __name__ == '__main__':
    unittest.main()
