from fake_toolbox import FakeToolbox
from scenario_generator import generate_scenario_from_high_level_summary, load_high_level_summary
import os

def main():
    summary_files = [f for f in os.listdir('scenarios/') if f.endswith(('.yaml', '.yml', '.md'))]
    
    for summary_file in summary_files:
        print(f"Loading high-level summary: {summary_file}")
        summary = load_high_level_summary(os.path.join('scenarios', summary_file))
        scenario = generate_scenario_from_high_level_summary(summary)
        
        toolbox = FakeToolbox(scenario)
        
        pod_details = toolbox.get_tool("get_pod_details")(scenario['cluster_name'], "backend-pod-xyz789", scenario['namespace'])
        print(pod_details.output)
        
        logs = toolbox.get_tool("get_logs_for_pod")(scenario['cluster_name'], "backend-pod-xyz789", scenario['namespace'])
        print(logs.output)

if __name__ == "__main__":
    main()