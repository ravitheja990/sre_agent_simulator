import os
import yaml
import markdown
from bs4 import BeautifulSoup
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
                    "```yaml\n"
                    "cluster_name: <cluster name>\n"
                    "namespace: <namespace>\n"
                    "pods:\n"
                    "  - name: <pod name>\n"
                    "    status: <status>\n"
                    "    restarts: <restarts>\n"
                    "    age: <age>\n"
                    "logs:\n"
                    "  - name: <log name>\n"
                    "    content: <log content>\n"
                    "```\n\n" + summary_str,
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

    # Expected scenario structure
    scenario = {
        "cluster_name": "main-cluster",
        "namespace": "default",
        "pods": [],
        "logs": []
    }

    # Attempt to parse the scenario text as YAML
    try:
        parsed_scenario = yaml.safe_load(scenario_text)
        
        if isinstance(parsed_scenario, dict):
            scenario["cluster_name"] = parsed_scenario.get("cluster_name", "main-cluster")
            scenario["namespace"] = parsed_scenario.get("namespace", "default")
            scenario["pods"] = parsed_scenario.get("pods", [])
            scenario["logs"] = parsed_scenario.get("logs", [])

            # Ensure pods and logs are in the correct format
            for pod in scenario["pods"]:
                if not all(key in pod for key in ["name", "status", "restarts", "age"]):
                    raise ValueError("Pod data is incomplete or improperly formatted")
            for log in scenario["logs"]:
                if not all(key in log for key in ["name", "content"]):
                    raise ValueError("Log data is incomplete or improperly formatted")

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
    summary = load_high_level_summary("high_level_summary1.yaml")
    scenario = generate_scenario_from_high_level_summary(summary)
    print(scenario)