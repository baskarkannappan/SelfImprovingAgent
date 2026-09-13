import logging
from litellm import embedding
from ..config import config

logger = logging.getLogger(__name__)

def generate_embedding(text: str) -> list[float]:
    """
    Generate a semantic vector embedding for the given text using the configured model.
    """
    try:
        # LiteLLM allows using ollama models via ollama/... or directly if base_url is set
        response = embedding(
            model=f"ollama/{config.EMBEDDING_MODEL}",
            input=[text],
            api_base=config.EMBEDDING_BASE_URL
        )
        return response.data[0]["embedding"]
    except Exception as e:
        logger.error(f"Failed to generate embedding: {e}")
        raise
