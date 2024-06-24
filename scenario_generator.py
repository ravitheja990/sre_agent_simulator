import os
import requests
import yaml
import markdown
from bs4 import BeautifulSoup

# Load LLaMA API key from environment variable
llama_api_key = os.getenv("LLAMA_API_KEY")
print("abc:", len(llama_api_key))
print("llama_api_key is ::",llama_api_key)
llama_api_url = "https://api.llama.ai/v1/models/llama"  # LLaMA API URL

def generate_scenario_from_high_level_summary(summary: str) -> dict:
    headers = {
        "Authorization": f"Bearer {llama_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": f"Generate a detailed scenario from the following high-level summary:\n\n{summary}",
        "max_tokens": 200
    }
    response = requests.post(llama_api_url, headers=headers, json=data)
    response.raise_for_status()
    scenario_text = response.json()["generated_text"].strip()
    scenario = yaml.safe_load(scenario_text)
    return scenario

def load_high_level_summary(file_path: str) -> str:
    with open(file_path, 'r') as file:
        if file_path.endswith('.yaml') or file_path.endswith('.yml'):
            summary = yaml.safe_load(file)
        elif file_path.endswith('.md'):
            html = markdown.markdown(file.read())
            summary = BeautifulSoup(html, features="html.parser").get_text()
        else:
            raise ValueError("Unsupported file format")
    return summary