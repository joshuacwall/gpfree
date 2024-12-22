from .base_agent import BaseAgent
from langchain.schema import SystemMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Union

class AgentState(TypedDict):
    messages: List[Union[SystemMessage]]

class PlainAgent(BaseAgent):
    """
    A simple agent that directly uses the LLM without any tools or complex workflows.
    Just takes user input, processes with system prompt, and returns response.
    """
    
    def get_tools(self):
        """No tools needed for plain agent"""
        return []

    def create(self):
        """Create a plain agent"""
        model = self.get_model()
        
        def call_model(state: AgentState, config: dict):
            """Node for calling the model"""
            system_msg = SystemMessage(content=self.config.system_prompt)
            response = model.invoke([system_msg] + state["messages"], config)
            return {"messages": [response]}

        # Create and compile the graph
        workflow = StateGraph(AgentState)
        
        # Add single node
        workflow.add_node("agent", call_model)
        
        # Set entry point
        workflow.set_entry_point("agent")
        
        # Add edge to end
        workflow.add_edge("agent", END)
        
        return workflow.compile() 