from typing import Dict, Callable
import json
from tools.kubernetes_tools import get_pod_details, get_logs_for_pod

class ToolOutput:
    def __init__(self, output: str):
        self.output = output

class FakeToolbox:
    def __init__(self, scenario: Dict):
        self.scenario = scenario

    def get_tool(self, tool_name: str) -> Callable:
        if tool_name == "get_pod_details":
            return self._get_pod_details
        elif tool_name == "get_logs_for_pod":
            return self._get_logs_for_pod

    def _get_pod_details(self, cluster_name: str, pod_name: str, namespace: str, summarize: bool = True) -> ToolOutput:
        return get_pod_details(cluster_name, pod_name, namespace, summarize)

    def _get_logs_for_pod(self, cluster_name: str, pod_name: str, namespace: str, compress: bool = False) -> ToolOutput:
        return get_logs_for_pod(cluster_name, pod_name, namespace, compress)

# Example usage
if __name__ == "__main__":
    scenario = {"cluster_name": "main-cluster", "namespace": "default"}
    toolbox = FakeToolbox(scenario)
    pod_details = toolbox.get_tool("get_pod_details")("main-cluster", "frontend-pod-abc123", "default")
    print(pod_details.output)
