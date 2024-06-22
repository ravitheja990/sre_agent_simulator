import json
from typing import Dict

class ToolOutput:
    def __init__(self, output: str):
        self.output = output

def get_pod_details(cluster_name: str, pod_name: str, namespace: str, summarize: bool = True) -> ToolOutput:
    output = {
        "cluster_name": cluster_name,
        "pod_name": pod_name,
        "namespace": namespace,
        "status": "Running",
        "restarts": 3,
        "age": "3d",
    }
    return ToolOutput(output=json.dumps(output))

def get_logs_for_pod(cluster_name: str, pod_name: str, namespace: str, compress: bool = False) -> ToolOutput:
    logs = [
        "2024-06-10 10:00:00 Error: Out of memory",
        "2024-06-10 10:05:00 Restarting pod",
    ]
    if compress:
        logs = [log.replace(" ", "") for log in logs]
    return ToolOutput(output=json.dumps(logs))
