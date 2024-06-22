from fake_toolbox.py import FakeToolbox
from scenario_generator import generate_scenario, load_scenario

def main():
    base_scenario = load_scenario('scenarios/scenario1.yaml')
    scenario = generate_scenario(base_scenario)
    
    toolbox = FakeToolbox(scenario)
    
    pod_details = toolbox.get_tool("get_pod_details")("main-cluster", "frontend-pod-abc123", "default")
    print(pod_details.output)
    
    logs = toolbox.get_tool("get_logs_for_pod")("main-cluster", "frontend-pod-abc123", "default")
    print(logs.output)

if __name__ == "__main__":
    main()
