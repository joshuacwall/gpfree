from typing import List
from .tavily_tool import tavily_tool
from .dnd_tool import dnd_rules_tool

# Registry of all available tools
AVAILABLE_TOOLS = {
    "tavily_tool": tavily_tool,
}

def get_tools(tool_names: List[str]):
    """Get tool instances by their names"""
    tools = []
    for name in tool_names:
        if name in AVAILABLE_TOOLS:
            tools.append(AVAILABLE_TOOLS[name])
    return tools 