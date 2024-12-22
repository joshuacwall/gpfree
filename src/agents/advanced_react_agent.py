from typing import Sequence, TypedDict, Annotated, Union, List
from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.runnables import RunnableConfig
from .base_agent import BaseAgent, AgentConfig
import json
from langchain.schema import HumanMessage

class AgentState(TypedDict):
    """The state of the agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    collected_info: List[str]

class AdvancedReactAgent(BaseAgent):
    """
    A ReAct agent that uses two LLMs:
    1. Router LLM determines whether to use tools or generate final response
    2. If tools are needed, executes them and returns to router
    3. If final response needed, passes to Response LLM for detailed answer
    """
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        # Override router model with fast model for routing decisions
        self.router_model = self._create_traced_model("llama3-groq-70b-8192-tool-use-preview")
        # Use the configured model (typically more powerful) for responses
        self.response_model = self._create_traced_model(self.config.model_id)

    def get_tools(self):
        """Get tools specified in config"""
        from tools.tool_registry import get_tools
        return get_tools(self.config.tools)

    def create(self):
        """Create a Router agent"""
        tools = self.get_tools()
        tools_by_name = {tool.name: tool for tool in tools}
        
        # Bind tools to router model (the faster one)
        router_model = self.router_model.bind_tools(tools)
        response_model = self.response_model
        
        def router_node(state: AgentState, config: RunnableConfig):
            """Node for routing decisions"""
            system_msg = SystemMessage(content="""
            You are a routing agent. Your job is to either:
            1. Use tools to gather information (respond with tool calls)
            2. Signal that you have enough information (respond with "FINAL_ANSWER")
            
            Only respond with "FINAL_ANSWER" when you have all needed information.
            """)
            
            # Initialize collected_info if not present
            if "collected_info" not in state:
                state["collected_info"] = []
            
            response = router_model.invoke([system_msg] + state["messages"], config)
            return {"messages": [response], "collected_info": state["collected_info"]}

        def tool_node(state: AgentState):
            """Node for executing tools"""
            outputs = []
            for tool_call in state["messages"][-1].tool_calls:
                tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
                state["collected_info"].append(f"{tool_call['name']}: {tool_result}")
                outputs.append(
                    ToolMessage(
                        content=json.dumps(tool_result),
                        name=tool_call["name"],
                        tool_call_id=tool_call["id"],
                    )
                )
            return {"messages": outputs, "collected_info": state["collected_info"]}

        def response_node(state: AgentState, config: RunnableConfig):
            """Node for generating final response"""
            collected_info_text = "\n".join(state["collected_info"])
            system_msg = SystemMessage(content=f"""
            You are a response generator. Using the collected information, 
            provide a detailed and helpful response to the user's query.
            
            Collected Information:
            {collected_info_text}
            """)
            
            # Get the user's original query (last message)
            user_query = state["messages"][-1].content
            
            # Create a new message list with just the system message and query
            messages = [system_msg, HumanMessage(content=user_query)]
            
            response = response_model.invoke(messages, config)
            return {"messages": [response], "collected_info": state["collected_info"]}

        def should_continue(state: AgentState):
            """Edge condition for determining next node"""
            last_message = state["messages"][-1]
            if "FINAL_ANSWER" in last_message.content:
                return "respond"
            if not last_message.tool_calls:
                return "respond"
            return "continue"
            
        # Create and compile the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("router", router_node)
        workflow.add_node("tools", tool_node)
        workflow.add_node("response", response_node)
        
        # Set entry point
        workflow.set_entry_point("router")
        
        # Add edges
        workflow.add_conditional_edges(
            "router",
            should_continue,
            {
                "continue": "tools",
                "respond": "response"
            }
        )
        workflow.add_edge("tools", "router")
        workflow.add_edge("response", END)
        
        return workflow.compile() 