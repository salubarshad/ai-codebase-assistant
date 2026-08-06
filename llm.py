from tool_registry import tools

def call_llm(client, messages):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools,
    )

    return response