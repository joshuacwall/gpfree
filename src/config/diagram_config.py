from typing import Dict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict, List
from typing_extensions import TypedDict

class AgentState(TypedDict):
    messages: Annotated[List[str], add_messages]

def get_agent_graph(agent_type: str) -> tuple[str, bytes]:
    """Dynamically create and return agent graph and description"""
    descriptions = {
        "plain": """
        A simple agent that directly uses the LLM without any tools or complex workflows.
        Just takes user input, processes with system prompt, and returns response.
        """,
        "react": """
        A ReAct agent that follows a simple workflow:
        1. Agent receives input and determines if tools are needed
        2. If tools are needed, executes them and returns results
        3. Process continues until completion
        """,
        "react_human": """
        A ReAct agent with human-in-the-loop capabilities that:
        1. Agent determines if tools are needed
        2. If tools needed, waits for human approval
        3. Upon approval, executes tools and returns to agent
        4. Upon rejection, returns to agent for alternative approach
        """,
        "advanced_react": """
        A ReAct agent that uses two LLMs:
        1. Router LLM determines whether to use tools or generate final response
        2. If tools are needed, executes them and returns to router
        3. If final response needed, passes to Response LLM for detailed answer
        """
    }
    
    if agent_type not in descriptions:
        raise ValueError(f"Unknown agent type: {agent_type}")
    
    # Create graph
    workflow = StateGraph(AgentState)
    
    # Add nodes and edges based on agent type
    if agent_type == "plain":
        workflow.add_node("agent", lambda x: x)
        workflow.set_entry_point("agent")
        workflow.add_edge("agent", END)
        
    elif agent_type == "react":
        workflow.add_node("agent", lambda x: x)
        workflow.add_node("tools", lambda x: x)
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent",
            lambda x: "complete" if x else "continue",
            {
                "complete": END,
                "continue": "tools"
            }
        )
        workflow.add_edge("tools", "agent")
        
    elif agent_type == "react_human":
        workflow.add_node("agent", lambda x: x)
        workflow.add_node("human_approval", lambda x: x)
        workflow.add_node("tools", lambda x: x)
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent",
            lambda x: "complete" if x else "approval",
            {
                "complete": END,
                "approval": "human_approval"
            }
        )
        workflow.add_conditional_edges(
            "human_approval",
            lambda x: "approved" if x else "rejected",
            {
                "approved": "tools",
                "rejected": "agent"
            }
        )
        workflow.add_edge("tools", "agent")
        
    elif agent_type == "advanced_react":
        workflow.add_node("router", lambda x: x)
        workflow.add_node("tools", lambda x: x)
        workflow.add_node("response", lambda x: x)
        workflow.set_entry_point("router")
        workflow.add_conditional_edges(
            "router",
            lambda x: "continue" if x else "respond",
            {
                "continue": "tools",
                "respond": "response"
            }
        )
        workflow.add_edge("tools", "router")
        workflow.add_edge("response", END)
    
    # Generate PNG using default LangGraph visualization
    graph = workflow.compile().get_graph()
    return descriptions[agent_type], graph.draw_mermaid_png()