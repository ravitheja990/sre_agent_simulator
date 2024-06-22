import random
import yaml

def generate_scenario(base_scenario):
    scenario = base_scenario.copy()
    scenario['log_names'] = [f"log-{i}" for i in range(5)]
    return scenario

def load_scenario(file_path):
    with open(file_path, 'r') as file:
        scenario = yaml.safe_load(file)
    return scenario

base_scenario = load_scenario('scenarios/scenario1.yaml')
scenario = generate_scenario(base_scenario)
print(scenario)
