import json
import logging
import requests
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ScenarioBuilder:
    def __init__(self, base_url=None):
        self.scenarios = []
        self.base_url = base_url

    def add_scenario(self, name, method, path, payload, expected_outcome):
        """Adds a new scenario to the list."""
        scenario = {
            'name': name,
            'method': method,
            'path': path,
            'payload': payload,
            'expected_outcome': expected_outcome
        }
        self.scenarios.append(scenario)
        logging.info(f"Scenario added: {name}")

    def save_scenarios_to_file(self, file_path):
        """Saves the scenarios to a JSON file."""
        try:
            with open(file_path, 'w') as file:
                json.dump(self.scenarios, file, indent=4)
            logging.info(f"Scenarios saved to {file_path}")
        except IOError as e:
            logging.error(f"Failed to save scenarios: {e}")

    def load_scenarios_from_file(self, file_path):
        """Loads scenarios from a JSON file."""
        try:
            with open(file_path, 'r') as file:
                self.scenarios = json.load(file)
            logging.info(f"Scenarios loaded from {file_path}")
        except IOError as e:
            logging.error(f"Failed to load scenarios: {e}")

    def run_scenario(self, scenario_name):
        """Runs a specific scenario by name."""
        scenario = next((s for s in self.scenarios if s['name'] == scenario_name), None)
        if scenario:
            # Example for HTTP request scenario execution
            full_url = urljoin(self.base_url, scenario['path'])
            response = requests.request(scenario['method'], full_url, data=scenario['payload'])
            if response.text == scenario['expected_outcome']:
                logging.info(f"Scenario '{scenario_name}' executed successfully with expected outcome.")
            else:
                logging.error(f"Scenario '{scenario_name}' did not produce the expected outcome.")
        else:
            logging.error(f"Scenario not found: {scenario_name}")

# Example usage
if __name__ == "__main__":
    builder = ScenarioBuilder(base_url='http://example.com/')
    builder.add_scenario('SQL Injection', 'POST', '/api/data', {'input': 'UNION SELECT'}, 'Data leak')
    # ... add more scenarios
    builder.save_scenarios_to_file('scenarios.json')
    builder.run_scenario('SQL Injection')
