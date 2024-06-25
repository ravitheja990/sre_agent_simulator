import unittest
from scenario_generator import generate_scenario_from_high_level_summary, load_high_level_summary
import yaml

class TestScenarioGenerator(unittest.TestCase):

    def test_load_high_level_summary_yaml(self):
        summary = load_high_level_summary('scenarios/high_level_summary1.yaml')
        self.assertIn('summary', summary)

    def test_generate_scenario_from_high_level_summary(self):
        summary = load_high_level_summary('scenarios/high_level_summary1.yaml')
        scenario = generate_scenario_from_high_level_summary(summary)
        self.assertIn('cluster_name', scenario)
        self.assertIn('namespace', scenario)
        self.assertIn('pods', scenario)
        self.assertIn('logs', scenario)

    def test_generate_scenario_structure(self):
        summary = {
            'summary': 'A test scenario for unit testing.'
        }
        scenario = generate_scenario_from_high_level_summary(summary)
        self.assertIsInstance(scenario, dict)
        self.assertIn('cluster_name', scenario)
        self.assertIn('namespace', scenario)
        self.assertIn('pods', scenario)
        self.assertIn('logs', scenario)

if __name__ == '__main__':
    unittest.main()
