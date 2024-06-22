README
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
1. Install dependencies: `pip install -r requirements.txt`
2. Run the main script: `python main.py`
3. Run tests: `python -m unittest discover tests`

## Adding Scenarios
- Add new scenario files in the `scenarios/` directory in YAML format.

## Adding Tools
- Implement new tool functions in the `tools/` directory and map them in `fake_toolbox.py`.
