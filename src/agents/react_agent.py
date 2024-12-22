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

class ReactAgent(BaseAgent):
    """
    A ReAct agent that follows a simple workflow:
    1. Agent receives input and determines if tools are needed
    2. If tools are needed, executes them and returns results
    3. Process continues until completion
    """
    
    def get_tools(self):
        """Get tools specified in config"""
        from tools.tool_registry import get_tools
        return get_tools(self.config.tools)

    def create(self):
        """Create a ReAct agent"""
        # Get tools and create name mapping
        tools = self.get_tools()
        tools_by_name = {tool.name: tool for tool in tools}
        
        # Bind tools to model
        model = self.get_model().bind_tools(tools)
        
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
            return {"messages": outputs}

        def call_model(state: AgentState, config: RunnableConfig):
            """Node for calling the model"""
            system_msg = SystemMessage(content=self.config.system_prompt)
            response = model.invoke([system_msg] + state["messages"], config)
            return {"messages": [response]}

        def should_continue(state: AgentState):
            """Edge condition for determining next node"""
            last_message = state["messages"][-1]
            if not last_message.tool_calls:
                return "end"
            return "continue"
            
        # Create and compile the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", call_model)
        workflow.add_node("tools", tool_node)
        
        # Set entry point
        workflow.set_entry_point("agent")
        
        # Add edges
        workflow.add_conditional_edges(
            "agent",
            should_continue,
            {
                "continue": "tools",
                "end": END,
            }
        )
        workflow.add_edge("tools", "agent")
        
        return workflow.compile() 