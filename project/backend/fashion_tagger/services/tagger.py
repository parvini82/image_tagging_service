"""Image tagging service layer.

Provides the public API for image analysis using the LangGraph pipeline.
This function returns raw LangGraph output without modification.
"""

from typing import Dict, Any
import logging

from .langgraph_integration.langgraph_service import run_langgraph_on_url

logger = logging.getLogger(__name__)


def generate_tags(image_url: str) -> Dict[str, Any]:
    """Generate tags for an image using the LangGraph pipeline.
    
    This function returns raw LangGraph output without modification.
    The LangGraph output is fully dynamic and contains whatever tags
    the pipeline produces. No normalization, filtering, or schema
    enforcement is applied.
    
    Uses advanced_reasoning mode with vision model, serpapi search,
    and translation enabled.
    
    Args:
        image_url: Public URL of the product image to analyze
    
    Returns:
        Raw LangGraph output as-is. On any exception, returns an empty dict {}.
    """
    try:
        result = run_langgraph_on_url(image_url)
        return result
    except Exception as e:
        logger.error(
            "Error while generating tags for %s: %s",
            image_url,
            str(e),
            exc_info=True,
        )
        return {}
