import os
import yaml
import markdown
from bs4 import BeautifulSoup
import json
import google.generativeai as genai

# Configure the Google Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def generate_scenario_from_high_level_summary(summary: dict) -> dict:
    # Convert summary dictionary to string
    summary_str = yaml.dump(summary)

    # Debug: Print the summary string
    print("Summary String:\n", summary_str)

    # Start a new chat session with the model
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "Generate a detailed scenario from the following high-level summary formatted in YAML. "
                    "The output should be in the following YAML format without any Markdown formatting:\n"
                    "cluster_name: <cluster name>\n"
                    "namespace: <namespace>\n"
                    "pods:\n"
                    "  - name: <pod name>\n"
                    "    status: <status>\n"
                    "    restarts: <restarts>\n"
                    "    age: <age>\n"
                    "logs:\n"
                    "  - name: <log name>\n"
                    "    content: <log content>\n\n" + summary_str,
                ],
            },
        ]
    )

    # Send the message to the model and get the response
    response = chat_session.send_message("Continue the scenario.")

    # Extract the generated scenario text
    scenario_text = response.text.strip()

    # Debug: Print the scenario text to inspect its content
    print("Generated Scenario Text:\n", scenario_text)

    # Remove any Markdown code block formatting (```yaml ... ```)
    if scenario_text.startswith("```yaml"):
        scenario_text = scenario_text[7:]
    if scenario_text.endswith("```"):
        scenario_text = scenario_text[:-3]

    # Debug: Print the cleaned scenario text
    print("Cleaned Scenario Text:\n", scenario_text)

    # Initialize scenario dictionary
    scenario = {}

    # Attempt to parse the scenario text as YAML
    try:
        parsed_scenario = yaml.safe_load(scenario_text)
        
        if isinstance(parsed_scenario, dict):
            scenario = parsed_scenario
        else:
            raise ValueError("Parsed scenario is not a dictionary")

    except (yaml.YAMLError, ValueError) as e:
        print("Parsing error:", e)
        # Debug: Print the exact scenario text that caused the error
        print("Failed Scenario Text:\n", scenario_text)
        scenario = {"error": "Failed to parse scenario text", "content": scenario_text}

    return scenario

def load_high_level_summary(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        if file_path.endswith('.yaml') or file_path.endswith('.yml'):
            summary = yaml.safe_load(file)
        elif file_path.endswith('.md'):
            html = markdown.markdown(file.read())
            summary = BeautifulSoup(html, features="html.parser").get_text()
            summary = {"content": summary}  # Wrap text content in a dictionary
        else:
            raise ValueError("Unsupported file format")
    return summary

# Example usage
if __name__ == "__main__":
    summary_files = [f for f in os.listdir('scenarios/') if f.endswith(('.yaml', '.yml', '.md'))]
    
    for summary_file in summary_files:
        print(f"Loading high-level summary: {summary_file}")
        summary = load_high_level_summary(os.path.join('scenarios', summary_file))
        scenario = generate_scenario_from_high_level_summary(summary)
        
        # Print the scenario as a JSON string for readability
        print("Generated Scenario:\n", json.dumps(scenario, indent=4))

        # Proceed with the scenario as a dictionary for processing
        toolbox = FakeToolbox(scenario)
        
        pod_details = toolbox.get_tool("get_pod_details")(scenario['cluster_name'], "backend-pod-xyz789", scenario['namespace'])
        print(pod_details.output)
        
        logs = toolbox.get_tool("get_logs_for_pod")(scenario['cluster_name'], "backend-pod-xyz789", scenario['namespace'])
        print(logs.output)
