from typing import Dict
from langgraph.graph import Graph
import importlib
import inspect
from agents.react_agent import ReactAgent
from agents.react_human_agent import ReactHumanAgent
from agents.advanced_react_agent import AdvancedReactAgent
from agents.plain_agent import PlainAgent

def get_agent_graph(agent_type: str) -> tuple[str, Graph]:
    """Dynamically create and return agent graph and description"""
    
    agent_classes = {
        "react": ReactAgent,
        "react_human": ReactHumanAgent,
        "advanced_react": AdvancedReactAgent,
        "plain": PlainAgent
    }
    
    if agent_type not in agent_classes:
        raise ValueError(f"Unknown agent type: {agent_type}")
        
    # Get agent class and docstring
    agent_class = agent_classes[agent_type]
    description = inspect.getdoc(agent_class) or "No description available"
    
    # Create minimal config for graph generation
    from config.agent_config import AgentConfig
    config = AgentConfig(
        name="temp",
        agent_type=agent_type,
        model_id="llama-3.3-70b-versatile",
        icon="🤖",
        tools=[]
    )
    
    # Create agent instance and get graph
    agent = agent_class(config)
    graph = agent.create().get_graph()
    
    return description, graph 