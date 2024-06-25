# SRE Agent Simulator

## Overview
The SRE Agent Simulator is designed to create synthetic environments for training an AI SRE agent to diagnose and solve issues in production environments.

## Structure
- `scenarios/`: Contains high-level scenario descriptions in YAML format.
- `tools/`: Contains tool functions that mimic real API behaviors.
- `tests/`: Contains unit tests for the tool functions.
- `fake_toolbox.py`: Provides a class to map tool names to their implementations.
- `scenario_generator.py`: Generates specific scenarios based on high-level descriptions.
- `main.py`: Main script to run the simulator.
- `requirements.txt`: Lists project dependencies.

## Usage

### Setup
1. **Add GEMINI API KEY and Create and activate a virtual environment**:
    ```bash
    export GEMINI_API_KEY="enter your API key here"
    python3 -m venv venv
    source venv/bin/activate
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Simulator
3. **Run the main script**:
    ```bash
    python3 main.py
    ```

### Running Tests
4. **Run tests**:
    ```bash
    python3 -m unittest discover tests
    ```

## Adding Scenarios
- Add new scenario files in the `scenarios/` directory in YAML format. Each file should follow the structure of the existing scenarios.

## Adding Tools
- Implement new tool functions in the `tools/` directory and map them in `fake_toolbox.py`.

## Example Scenario
Here's an example of what a scenario file might look like (`scenarios/high_level_summary1.yaml`):

```yaml
summary: |
  An e-commerce store deployed to GCP.
  Has a PostgreSQL, a backend, and a frontend all running in a single Kubernetes cluster.
  Has a Datadog agent in the same Kubernetes cluster.
  Has a Datadog API where logs for all systems are served and queryable.
  The system has been running from date 2024-06-10 to 2024-06-20 for all services, meaning logs and metadata should be available from them.
  The backend has 3 restarts. These restarts should be shown in tool calls to the Kubernetes tools as well as Datadog logs. The logs show an out of memory problem.
  There are no other problems in this environment.
