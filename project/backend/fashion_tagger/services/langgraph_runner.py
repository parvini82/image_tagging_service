"""Thin service wrapper for LangGraph image tagging.

This module provides a minimal wrapper around the LangGraph workflow
without any business logic or output modification.
"""

from typing import Dict, Any
import logging

from .langgraph_integration.langgraph_service import run_langgraph_on_url

logger = logging.getLogger(__name__)


def run_image_tagger(image_url: str) -> Dict[str, Any]:
    """Run the LangGraph image tagging pipeline.
    
    This is a thin wrapper that calls the LangGraph workflow and handles
    exceptions. It does not modify, normalize, or restructure the output.
    
    Uses advanced_reasoning mode with vision model, serpapi search,
    and translation enabled.
    
    Args:
        image_url: Public URL of the product image to analyze
    
    Returns:
        Dict with keys:
        - 'english': English tags from LangGraph
        - 'persian': Persian tags from LangGraph
        
        On failure, returns empty dicts: {"english": {}, "persian": {}}
    """
    try:
        result = run_langgraph_on_url(image_url)
        return result
    except Exception as e:
        logger.error(
            "Error in LangGraph image tagging pipeline for %s: %s",
            image_url,
            str(e),
            exc_info=True,
        )
        return {"english": {}, "persian": {}}
