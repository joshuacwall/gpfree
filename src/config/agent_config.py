from dataclasses import dataclass
from typing import List, Optional, Literal
from config.model_config import ModelConfig

@dataclass
class AgentConfig:
    name: str
    agent_type: Literal["react", "react_human", "advanced_react", "plain"]
    model_id: str
    icon: str
    temperature: float = 0.7
    system_prompt: str = ""
    tools: List[str] = None

    def get_model_config(self, model_id: str = None) -> ModelConfig:
        """Get the full model configuration"""
        from config.model_config import get_model_by_id
        return get_model_by_id(model_id or self.model_id)

# Example configurations
DEFAULT_AGENTS = {
    "Simple Chat": AgentConfig(
        name="Simple Chat",
        agent_type="plain",
        model_id="llama-3.3-70b-versatile",
        icon="🤖",
        system_prompt="",
    ),
    "Coach Theo": AgentConfig(
        name="Theo",
        agent_type="react",
        model_id="llama-3.3-70b-versatile",
        icon="🏀",
        system_prompt="You are Theo, a basketball coach and anylst. You like to repond with come on son when someone says something ridiculous.",
        tools=["tavily_tool"]
    ),
    "Quest Craft": AgentConfig(
        name="Quest Craft",
        agent_type="react",
        model_id="llama-3.3-70b-versatile",
        icon="🗡️",
        system_prompt="You are a helpful AI assistant for Dungeons & Dragons. Your role is to assist players and Dungeon Masters with rules, dice rolls, and general gameplay questions.",
        tools=["tavily_tool"]
    ),    
    "Crypto Pal": AgentConfig(
        name="Crypto Pal",
        agent_type="react",
        model_id="llama-3.3-70b-versatile",
        icon="₿",
        system_prompt="You are a helpful AI assistant for Bitcoin. You are a Bitcoin expert and can answer any questions about Bitcoin or other crypto currencies.",
        tools=["tavily_tool"]
    )
} 