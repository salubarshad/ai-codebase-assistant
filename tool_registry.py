import tools

available_tools = {
    "get_project_name": tools.get_project_name,
    "add_numbers": tools.add_numbers,
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