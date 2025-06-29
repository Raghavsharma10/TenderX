import os
from dotenv import load_dotenv
import json
import requests
import re

# Load environment variables and Hugging Face token
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Define available tools
tools = [
    {
        "name": "get_country_by_name",
        "description": "Get info using country name",
        "parameters": {"name": "string", "fields": "list of fields"}
    },
    {
        "name": "get_country_by_capital",
        "description": "Search using capital",
        "parameters": {"capital": "string", "fields": "list of fields"}
    },
    {
        "name": "get_country_by_currency",
        "description": "Search using currency",
        "parameters": {"currency": "string", "fields": "list of fields"}
    },
    {
        "name": "get_country_by_language",
        "description": "Search using language",
        "parameters": {"language": "string", "fields": "list of fields"}
    },
    {
        "name": "get_countries_by_subregion",
        "description": "Get countries in a subregion",
        "parameters": {"subregion": "string", "fields": "list of fields"}
    }
]

def simple_tool_prompt(user_input: str) -> str:
    return f"""
Available tools:
{json.dumps(tools, indent=2)}

User query: "{user_input}"

Respond ONLY with a single-line JSON object in this format:
{{"tool_name": ..., "parameters": ...}}
Example:
{{"tool_name": "get_country_by_name", "parameters": {{"name": "France", "fields": ["population"]}}}}
"""

def reasoning_tool_prompt(user_input: str) -> str:
    return f"""
You are a reasoning agent. Analyze the user's question and decide what to fetch using one of the available tools.

Available tools:
{json.dumps(tools, indent=2)}

Return only a valid JSON like:
{{"tool_name": ..., "parameters": ...}}

User query:
"{user_input}"

Only return a single JSON object. Do not explain or add code.
"""

def select_tool_with_llm(user_input: str) -> dict | None:
    url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    prompt = simple_tool_prompt(user_input)

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 256, "do_sample": True}
    }

    response = requests.post(url, headers=headers, json=payload)
    output = response.json()
    try:
        gen = output[0]["generated_text"]
        print("🧪 Raw output from LLM:\n", gen)
        
        #Try multiple strategies to extract JSON
        # Strategy 1: Look for JSON patterns with regex
        matches = re.findall(r'(\{.*?\})', gen, re.DOTALL)
        for match in matches:
            try:
                data = json.loads(match)
                if "tool_name" in data and "parameters" in data:
                    return data
            except json.JSONDecodeError:
                continue
        
        #Look for the last occurrence of a JSON-like structure
        # Find the last line that starts with {
        lines = gen.split('\n')
        for line in reversed(lines):
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                try:
                    data = json.loads(line)
                    if "tool_name" in data and "parameters" in data:
                        return data
                except json.JSONDecodeError:
                    continue
        
         #Try to extract JSON from the end of the response
        # Look for the last complete JSON object
        last_brace = gen.rfind('}')
        if last_brace != -1:
            # Find the matching opening brace
            brace_count = 0
            start_pos = last_brace
            for i in range(last_brace, -1, -1):
                if gen[i] == '}':
                    brace_count += 1
                elif gen[i] == '{':
                    brace_count -= 1
                    if brace_count == 0:
                        start_pos = i
                        break
            
            if start_pos != last_brace:
                json_str = gen[start_pos:last_brace + 1]
                try:
                    data = json.loads(json_str)
                    if "tool_name" in data and "parameters" in data:
                        return data
                except json.JSONDecodeError:
                    pass
        
        print("No valid JSON found in any extracted block.")
        print("Raw output:", gen)
        return None
    except Exception as e:
        print("Error parsing model output:", e)
        print("Raw output:", output)
        return None

def synthesize_answer_with_llm(prompt: str) -> str:
    url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 300, "do_sample": True}
    }

    response = requests.post(url, headers=headers, json=payload)
    output = response.json()
    try:
        return output[0]["generated_text"].strip()
    except Exception as e:
        print("Error parsing synthesized output:", e)
        print("Raw output:", output)
        return "Sorry, I couldn't generate a summary."
    
def analyze_query_intent(user_query: str) -> dict | None:
    return select_tool_with_llm(user_query)