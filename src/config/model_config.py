from dataclasses import dataclass
from typing import Dict, Literal

@dataclass
class ModelConfig:
    provider: Literal["groq"]
    max_temperature: float
    default_temperature: float
    description: str
    media: Literal["text-only", "text-and-image", "image-only"]
    cost_per_1k: float
    context_length: int

# Available models configuration
AVAILABLE_MODELS = {
    "llama-3.3-70b-versatile": ModelConfig(
        provider="groq",
        max_temperature=1.0,
        default_temperature=0.7,
        description="High-performance open source model, good for general tasks",
        media="text-only",
        cost_per_1k=0.0007,
        context_length=8192
    ),
    "llama3-groq-8b-8192-tool-use-preview": ModelConfig(
        provider="groq",
        max_temperature=1.0,
        default_temperature=0.7,
        description="Small model, fine tuned for tool routing",
        media="text-only",
        cost_per_1k=0.0007,
        context_length=8192
    ),
    "llama3-groq-70b-8192-tool-use-preview": ModelConfig(
        provider="groq",
        max_temperature=1.0,
        default_temperature=0.7,
        description="Large model, fine tuned for tool routing",
        media="text-only",
        cost_per_1k=0.0007,
        context_length=8192
    )
}

def get_model_by_id(model_id: str) -> ModelConfig:
    """Get model config by its ID"""
    if model_id not in AVAILABLE_MODELS:
        raise ValueError(f"Model {model_id} not found")
    return AVAILABLE_MODELS[model_id]

def get_models_by_provider(provider: str) -> Dict[str, ModelConfig]:
    """Get all models for a specific provider"""
    return {k: v for k, v in AVAILABLE_MODELS.items() if v.provider == provider} 