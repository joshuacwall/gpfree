from typing import Sequence, TypedDict, Annotated
from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.runnables import RunnableConfig
from .base_agent import BaseAgent
import json

class AgentState(TypedDict):
    """The state of the agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    human_approved: bool

class ReactHumanAgent(BaseAgent):
    """
    A ReAct agent with human-in-the-loop capabilities that pauses for approval
    before executing tools.
    """
    
    def get_tools(self):
        """Get tools specified in config"""
        from tools.tool_registry import get_tools
        return get_tools(self.config.tools)
    
    def create(self):
        """Create a custom ReAct agent with human approval"""
        # Get tools and create name mapping
        tools = self.get_tools()
        tools_by_name = {tool.name: tool for tool in tools}
        
        # Bind tools to model
        model = self.get_model().bind_tools(tools)
        
        def call_model(state: AgentState, config: RunnableConfig):
            """Node for calling the model"""
            system_msg = SystemMessage(content=self.config.system_prompt)
            response = model.invoke([system_msg] + state["messages"], config)
            return {"messages": [response], "human_approved": False}
        
        def tool_node(state: AgentState):
            """Node for executing tools"""
            outputs = []
            for tool_call in state["messages"][-1].tool_calls:
                tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
                outputs.append(
                    ToolMessage(
                        content=json.dumps(tool_result),
                        name=tool_call["name"],
                        tool_call_id=tool_call["id"],
                    )
                )
            return {"messages": outputs, "human_approved": False}
        
        def should_continue(state: AgentState):
            """Edge condition for determining next node"""
            last_message = state["messages"][-1]
            if not last_message.tool_calls:
                return "end"
            return "human_approval"
        
        def human_approval(state: AgentState):
            """Node for human approval"""
            # In a real implementation, this would wait for human input
            # For visualization purposes, we'll auto-approve
            return {"human_approved": True}
        
        def check_approval(state: AgentState):
            """Edge condition for checking human approval"""
            if state["human_approved"]:
                return "execute"
            return "agent"
        
        # Create and compile the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", call_model)
        workflow.add_node("human_approval", human_approval)
        workflow.add_node("tools", tool_node)
        
        # Set entry point
        workflow.set_entry_point("agent")
        
        # Add edges
        workflow.add_conditional_edges(
            "agent",
            should_continue,
            {
                "human_approval": "human_approval",
                "end": END,
            }
        )
        workflow.add_conditional_edges(
            "human_approval",
            check_approval,
            {
                "execute": "tools",
                "agent": "agent"
            }
        )
        workflow.add_edge("tools", "agent")
        
        return workflow.compile()