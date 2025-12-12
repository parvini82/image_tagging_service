"""Image tagging service layer.

Provides the public API for image analysis using the LangGraph pipeline.
Handles normalization of LangGraph output to the API contract.
"""

from typing import Optional, Dict, Any
import logging

from .langgraph_integration.langgraph_service import run_langgraph_on_url
from .langgraph_integration.model_client import OpenRouterError

logger = logging.getLogger(__name__)


def _extract_tag_value(entity_list: list, entity_name: str) -> Optional[str]:
    """Extract the first value from an entity in the LangGraph output.
    
    Args:
        entity_list: List of entity dicts from LangGraph output
        entity_name: Name of the entity to extract (e.g., 'category', 'color')
    
    Returns:
        The first value of the entity, or None if not found
    """
    if not isinstance(entity_list, list):
        return None
    
    for entity in entity_list:
        if isinstance(entity, dict) and entity.get("name") == entity_name:
            values = entity.get("values", [])
            if values and len(values) > 0:
                return str(values[0]).lower().strip()
    
    return None


def generate_tags(image_url: str, mode: str = "advanced_reasoning") -> Dict[str, Optional[str]]:
    """Generate fashion tags for an image using the LangGraph pipeline.
    
    This is the primary public API for the tagging service.
    It handles the full pipeline: vision analysis -> normalization -> output.
    
    Args:
        image_url: Public URL of the product image to analyze
        mode: Processing mode - "fast" (default), "reasoning", "advanced_reasoning"
    
    Returns:
        Dict with keys:
        - 'category': Product category (e.g., 'shirt', 'dress') or None
        - 'color': Primary color (e.g., 'blue', 'red') or None
        - 'material': Main material (e.g., 'cotton', 'leather') or None
        
        Returns None values for any tags that could not be extracted.
    
    Raises:
        Gracefully handles all errors by returning None values rather than raising.
    """
    try:
        # Execute LangGraph pipeline
        result = run_langgraph_on_url(image_url, mode=mode)
        
        # Normalize output to API contract
        return result
    
    except OpenRouterError as e:
        logger.error("OpenRouter API error while processing %s: %s", image_url, str(e))
        return {"category": None, "color": None, "material": None}
    
    except Exception as e:
        logger.error(
            "Unexpected error while generating tags for %s: %s",
            image_url,
            str(e),
            exc_info=True,
        )
        return {"category": None, "color": None, "material": None}
