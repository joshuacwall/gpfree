from abc import ABC, abstractmethod
from config.agent_config import AgentConfig
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.chat_models import ChatLiteLLM


class BaseAgent(ABC):
    def __init__(self, config: AgentConfig):
        self.config = config
        # Initialize memory for all agents
        self.memory = MemorySaver()
        # Initialize primary model for all agents with tracing
        self.model = self._create_traced_model(self.config.model_id)
        # Initialize secondary model if specified
        self.secondary_model = None
        if hasattr(self.config, 'secondary_model_id') and self.config.secondary_model_id:
            self.secondary_model = self._create_traced_model(self.config.secondary_model_id)
        
    def _create_traced_model(self, model_id):
        """Create a traced model instance"""
        model_config = self.config.get_model_config(model_id)
        return ChatLiteLLM(
            model=f"{model_config.provider}/{model_id}",
            temperature=self.config.temperature
        )
    
    @abstractmethod
    def create(self):
        """Create and return the agent instance"""
        pass
    
    @abstractmethod
    def get_tools(self):
        """Get the tools for this agent"""
        pass
    
    def get_memory(self):
        """Get the memory instance for this agent"""
        return self.memory
    
    def get_model(self):
        """Get the primary model instance"""
        return self.model
        
    def get_secondary_model(self):
        """Get the secondary model instance"""
        return self.secondary_model