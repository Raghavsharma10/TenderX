# simple_agent.py

from api_wrapper import *
from tool_selector import analyze_query_intent, synthesize_answer_with_llm
import json


def main():
    # Keep taking user input until the user types 'exit' or 'quit'
    while True:
        user_query = input("\nAsk about a country: ").strip()
        if user_query.lower() in ["exit", "quit"]:
            break

        # Let the LLM figure out which API tool is best suited for the query
        tool_plan = analyze_query_intent(user_query)
        print("🔎 Raw tool plan:", tool_plan)

        # Handle empty or faulty plans
        if not tool_plan:
            print("Could not understand the query.")
            continue

        # Basic format check on tool plan
        if "tool_name" not in tool_plan or "parameters" not in tool_plan:
            print("Invalid tool plan format returned by the model.")
            continue

        tool_name = tool_plan["tool_name"]
        params = tool_plan["parameters"]

        # Make sure fields is always a list (even if LLM returns a single string)
        if isinstance(params.get("fields"), str):
            params["fields"] = [params["fields"]]

        print(f"🛠️  Calling {tool_name} with {params}")

        # Map tool names to actual Python functions
        tool_registry = {
            "get_country_by_name": get_country_by_name,
            "get_country_by_capital": get_country_by_capital,
            "get_country_by_currency": get_country_by_currency,
            "get_country_by_language": get_country_by_language,
            "get_countries_by_subregion": get_countries_by_subregion
        }

        tool_func = tool_registry.get(tool_name)
        if not tool_func:
            print("Tool not found.")
            continue

        # Call the selected tool (API) with given parameters
        api_response = tool_func(**params)
        if not api_response:
            print("API returned no data.")
            continue

        # Send both question and API response to LLM to generate a friendly answer
        final_answer = synthesize_answer_with_llm(f"""
You are an AI assistant.

User Question: "{user_query}"

API Response Data:
{api_response}

Generate a friendly, clear, and concise natural language answer:
""")

        # Output the final synthesized answer
        if not final_answer.strip():
            print("Sorry, I couldn't generate an answer.")
        else:
            print(f"\n💬 {final_answer}")


if __name__ == "__main__":
    main()