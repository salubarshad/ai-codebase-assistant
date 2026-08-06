import json

from prompts import SYSTEM_PROMPT
from tool_registry import available_tools
from llm import call_llm


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


def tool_summary(tool_call, tool_result):
    name = tool_call.function.name
    arguments = tool_call.function.arguments
    print(f"\nTool:\n{name}")
    print(f"\narguments:\n{arguments}")
    if name == "list_files":
        print(f"\nResult:\n{len(tool_result)} files found.")
    elif name == "read_file":
        print(f"\nResult:\nRead {len(tool_result.splitlines())} lines.")
    elif name == "search_codebase":
        print(f"\nResult:\n{len(tool_result)} matches found.")
    else:
        print(f"\nResult:\n{tool_result}")


def run_agent(client, prompt):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]
    response = call_llm(client, messages)

    print(f"\n===========================\nUser Question\n===========================\n\n{messages[1]["content"]}")
    iteration_no = 0

    MAX_ITERATIONS = 10
    for iteration in range(MAX_ITERATIONS):
        message = response.choices[0].message
        messages.append(message)

        iteration_no = iteration_no + 1
        print(f"\n===========================\nIteration {iteration_no}\n===========================")

        if not message.tool_calls:

            print("No tool calls.\n")
            print("Final Answer: ")

            return response

        tool_calls = message.tool_calls
        print(f"\nLLM Decision:\nRequested {len(tool_calls)} tool{"" if len(tool_calls) == 1 else "s"}.")

        for tool_call in tool_calls:
            tool_result = execute_tool(tool_call)
            tool_summary(tool_call, tool_result)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                }
            )

        response = call_llm(client, messages)

    raise "Maxium agent iterations exceeded."
