import streamlit as st
from config.agent_config import DEFAULT_AGENTS
from config.user_agents import get_user_agents, UserAgent, save_user_agent
from config.model_config import AVAILABLE_MODELS
from tools.tool_registry import AVAILABLE_TOOLS
from utils.session import create_new_session, get_current_session
from agents.react_agent import ReactAgent
from agents.react_human_agent import ReactHumanAgent
from agents.advanced_react_agent import AdvancedReactAgent
from config.diagram_config import get_agent_graph
from auth.auth import login
from styles.login import get_login_styles
from agents.plain_agent import PlainAgent

def render_sidebar():
    """Render the sidebar with agent controls"""
    with st.sidebar:
        st.title("🤖 Agent Control")
        tab1, tab2, tab3 = st.tabs(["Select Agent", "Create Agent", "Agent Architecture Diagrams"])
        
        with tab1:
            render_agent_selection()
        with tab2:
            render_agent_creation(tab2)
        with tab3:
            render_architecture_diagrams()

def render_agent_selection():
    """Render agent selection tab"""
    all_agents = {**DEFAULT_AGENTS, **get_user_agents()}
    agent_names = list(all_agents.keys())
    
    selected_agent = st.selectbox(
        "Select Agent",
        agent_names,
        key="agent_selector"
    )
    
    # Clear chat button with matching width
    if st.button("🗑️ Clear Chat", key="clear_chat", use_container_width=True):
        session_id, session = get_current_session()
        if session:
            session["messages"] = []
            st.rerun()
    
    # Handle new agent selection
    if selected_agent != st.session_state.current_session:
        agent_config = all_agents[selected_agent]
        agent_instance = create_agent_instance(agent_config)
        create_new_session(selected_agent, agent_config, agent_instance)

def create_agent_instance(agent_config):
    """Create appropriate agent instance based on type"""
    if agent_config.agent_type == "react":
        return ReactAgent(agent_config)
    elif agent_config.agent_type == "react_human":
        return ReactHumanAgent(agent_config)
    elif agent_config.agent_type == "advanced_react":
        return AdvancedReactAgent(agent_config)
    elif agent_config.agent_type == "plain":
        return PlainAgent(agent_config)
    else:
        raise ValueError(f"Unknown agent type: {agent_config.agent_type}")

def render_agent_creation(tab):
    """Render agent creation form"""
    with tab:
        st.subheader("Create New Agent")
        
        # Agent creation form
        with st.form("create_agent"):
            name = st.text_input("Agent Name")
            system_prompt = st.text_area("System Prompt", 
                help="Define the agent's personality and primary objective")
            
            # Agent type selection
            agent_type = st.selectbox(
                "Agent Type",
                options=["react", "plain"],
                help="Select the type of agent to create"
            )
            
            # Model selection with provider grouping
            selected_model = st.selectbox(
                "Model",
                options=list(AVAILABLE_MODELS.keys()),
                format_func=lambda x: f"{x} ({AVAILABLE_MODELS[x].provider.title()})",
                help="Select the model to power your agent"
            )
            # Get the selected model's config
            model_config = AVAILABLE_MODELS[selected_model]
            
            # Temperature slider with model-specific limits
            temperature = st.slider(
                "Temperature",
                0.0,
                model_config.max_temperature,
                model_config.default_temperature,
                0.1,
                help=f"Higher values make the output more random. Max: {model_config.max_temperature}"
            )
            
            # Show model info in an expander
            with st.expander("Model Information"):
                st.write(f"**Description:** {model_config.description}")
                st.write(f"**Context Length:** {model_config.context_length:,} tokens")
                st.write(f"**Cost:** ${model_config.cost_per_1k:.4f} per 1k tokens")
            
            # Tool selection
            available_tools = list(AVAILABLE_TOOLS.keys())
            selected_tools = st.multiselect(
                "Select Tools",
                available_tools,
                help="Choose the tools this agent can use"
            )
            
            # Add after model selection
            if agent_type == "router":
                secondary_model = st.selectbox(
                    "Response Model",
                    options=list(AVAILABLE_MODELS.keys()),
                    format_func=lambda x: f"{x} ({AVAILABLE_MODELS[x].provider.title()})",
                    help="Select the model to generate final responses"
                )
            # Submit button
            if st.form_submit_button("Create Agent"):
                if name and system_prompt:
                    new_agent = UserAgent(
                        name=name,
                        agent_type=agent_type,
                        model_id=selected_model,
                        icon="🤖",
                        temperature=temperature,
                        system_prompt=system_prompt,
                        tools=selected_tools
                    )
                    save_user_agent(new_agent)
                    st.success(f"Agent '{name}' created successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields")


def render_architecture_diagrams():
    """Render agent architecture diagrams"""
    try:
        import pygraphviz
        
        agent_type = st.selectbox(
            "Select Agent Type",
            options=["react", "react_human", "advanced_react", "plain"],
            help="View the workflow diagram for each agent type"
        )
        
        description, graph = get_agent_graph(agent_type)
        st.markdown(f"**{agent_type.title()} Agent**")
        st.markdown(description)
        st.image(graph.draw_png())
        
    except ImportError:
        st.error("""
        Missing required dependencies for graph visualization.
        Please install:
        ```bash
        pip install pygraphviz
        ```
        For system dependencies, see: https://github.com/pygraphviz/pygraphviz/blob/main/INSTALL.txt
        """)