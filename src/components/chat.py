import streamlit as st
from utils.session import get_current_session
from config.agent_config import DEFAULT_AGENTS
from config.user_agents import get_user_agents
from agents.react_agent import ReactAgent
from agents.react_human_agent import ReactHumanAgent
from agents.advanced_react_agent import AdvancedReactAgent
from agents.plain_agent import PlainAgent

def render_chat_interface():
    """Render the main chat interface"""
    username = st.session_state.username
    st.title(f"{username}'s GPFree")
    
    session_id, session = get_current_session()
    if not session_id:
        st.info("Please select an agent to start chatting!")
        return
        
    render_agent_info(session)
    render_chat_messages(session)
    handle_user_input(session)

def render_agent_info(session):
    """Render agent configuration information"""
    all_agents = {**DEFAULT_AGENTS, **get_user_agents()}
    agent_config = all_agents[session["agent"]]
    
    with st.expander("Agent Configuration", expanded=False):
        model_config = agent_config.get_model_config()
        st.write(f"Agent Type: {agent_config.agent_type}")
        st.write(f"Model: {agent_config.model_id} ({model_config.provider})")
        st.write(f"Temperature: {agent_config.temperature}")
        st.write(f"System Prompt: {agent_config.system_prompt}")
        st.write(f"Tools: {', '.join(agent_config.tools or [])}")

def render_chat_messages(session):
    """Render chat message history"""
    all_agents = {**DEFAULT_AGENTS, **get_user_agents()}
    agent_config = all_agents[session["agent"]]
    
    for message in session["messages"]:
        with st.chat_message(message["role"], avatar=agent_config.icon if message["role"] == "assistant" else None):
            st.markdown(message["content"])

def handle_user_input(session):
    """Handle user chat input and agent responses"""
    if prompt := st.chat_input("What would you like to know?"):
        all_agents = {**DEFAULT_AGENTS, **get_user_agents()}
        agent_config = all_agents[session["agent"]]
        
        # Add user message
        session["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Create agent instance
        if agent_config.agent_type == "react":
            agent_instance = ReactAgent(agent_config)
        elif agent_config.agent_type == "react_human":
            agent_instance = ReactHumanAgent(agent_config)
        elif agent_config.agent_type == "advanced_react":
            agent_instance = AdvancedReactAgent(agent_config)
        elif agent_config.agent_type == "plain":
            agent_instance = PlainAgent(agent_config)

        agent = agent_instance.create()
        
        # Show assistant is thinking
        with st.chat_message("assistant", avatar=agent_config.icon):
            message_placeholder = st.empty()
            message_placeholder.markdown("🤔 Thinking...")
            
            # Configure memory settings
            config = {
                "configurable": {
                    "thread_id": session["thread_id"],
                    "memory": session.get("memory")
                },
                "metadata": {
                    "agent_type": agent_config.agent_type,
                    "model": agent_config.model_id,
                    "temperature": agent_config.temperature
                }
            }
            
            # Get response from agent
            response = agent.invoke(
                {
                    "messages": [
                        *[("human" if m["role"] == "user" else "assistant", m["content"]) 
                          for m in session["messages"][:-1]],
                        ("user", prompt)
                    ],
                    "collected_info": []  # Initialize collected_info for advanced_react
                },
                config=config
            )
            
            # Extract the final message based on agent type
            if agent_config.agent_type == "advanced_react":
                final_message = response["messages"][-1]
                collected_info = response.get("collected_info", [])
                
                # Display collected information in an expander
                with st.expander("🔍 Information Collected", expanded=False):
                    for info in collected_info:
                        st.write(info)
            else:
                final_message = response["messages"][-1]
            
            # Update the message placeholder
            message_placeholder.markdown(final_message.content)
            
            # Update memory in session
            session["memory"] = config["configurable"]["memory"]
            
            # Add assistant message to chat history
            session["messages"].append(
                {"role": "assistant", "content": final_message.content}
            )
