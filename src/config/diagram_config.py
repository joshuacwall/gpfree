from typing import Dict
import inspect
import graphviz
from agents.react_agent import ReactAgent
from agents.react_human_agent import ReactHumanAgent
from agents.advanced_react_agent import AdvancedReactAgent
from agents.plain_agent import PlainAgent

def get_agent_graph(agent_type: str) -> tuple[str, graphviz.Digraph]:
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
    
    # Create graph
    dot = graphviz.Digraph(comment=agent_type)
    dot.attr(rankdir='TB')  # Top to Bottom direction
    
    # Define node styles
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')
    
    # Add start node
    dot.node('start', 'START', fillcolor='#90EE90', fontcolor='black')  # Light green
    
    # Add nodes and edges based on agent type
    if agent_type == "plain":
        dot.node('agent', 'Agent', fillcolor='#ADD8E6')  # Light blue
        dot.node('end', 'END', fillcolor='#FFB6C1')  # Light pink
        dot.edge('start', 'agent')
        dot.edge('agent', 'end')
    elif agent_type == "react":
        dot.node('agent', 'Agent', fillcolor='#ADD8E6')
        dot.node('tools', 'Tools', fillcolor='#DDA0DD')  # Light purple
        dot.node('end', 'END', fillcolor='#FFB6C1')
        dot.edge('start', 'agent')
        dot.edge('agent', 'tools')
        dot.edge('tools', 'agent')
        dot.edge('agent', 'end', 'complete')
    elif agent_type == "react_human":
        dot.node('agent', 'Agent', fillcolor='#ADD8E6')
        dot.node('human', 'Human\nApproval', fillcolor='#F0E68C')  # Khaki
        dot.node('tools', 'Tools', fillcolor='#DDA0DD')
        dot.node('end', 'END', fillcolor='#FFB6C1')
        dot.edge('start', 'agent')
        dot.edge('agent', 'human')
        dot.edge('human', 'tools', 'approved')
        dot.edge('tools', 'agent')
        dot.edge('human', 'agent', 'rejected')
        dot.edge('agent', 'end', 'complete')
    elif agent_type == "advanced_react":
        dot.node('router', 'Router', fillcolor='#ADD8E6')
        dot.node('tools', 'Tools', fillcolor='#DDA0DD')
        dot.node('response', 'Response', fillcolor='#98FB98')  # Pale green
        dot.node('end', 'END', fillcolor='#FFB6C1')
        dot.edge('start', 'router')
        dot.edge('router', 'tools', 'continue')
        dot.edge('tools', 'router')
        dot.edge('router', 'response', 'respond')
        dot.edge('response', 'end')
    
    return description, dot