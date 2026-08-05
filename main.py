import os
import json
from typing import Any

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)


def call_llm(messages):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools,
    )

    return response


def execute_tool(tool_call):
    tool_name = tool_call.function.name

    if tool_name not in available_tools:
        return f"Error: Unknown tool '{tool_name}'"

    tool_function = available_tools[tool_name]

    try:
        arguments = json.loads(tool_call.function.arguments or "null")
    except json.JSONDecodeError:
        return "Error: Tool arguments were not valid JSON."
    if arguments is None:
        arguments = {}

    try:
        tool_result = tool_function(**arguments)
    except Exception as e:
        return f"Error while executing tool: {e}"

    return str(tool_result)


def run_agent(prompt):
    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]
    response = call_llm(messages)

    MAX_ITERATIONS = 10
    for iteration in range(MAX_ITERATIONS):
        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            return response

        tool_calls = message.tool_calls

        for tool_call in tool_calls:
            tool_result = execute_tool(tool_call)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                }
            )

        response = call_llm(messages)

    raise "Maxium agent iterations exceeded."


def get_project_name():
    return "AI Codebase Assistant"


def add_numbers(a: int, b: int) -> int:
    return a + b


available_tools = {
    "get_project_name": get_project_name,
    "add_numbers": add_numbers,
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_project_name",
            "description": "Returns the name of the current project.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "Adds two numbers together.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "The first number",
                    },
                    "b": {
                        "type": "integer",
                        "description": "The second number",
                    },
                },
                "required": ["a", "b"],
            },
        },
    },
]

prompt = input("Ask a question: \n")
