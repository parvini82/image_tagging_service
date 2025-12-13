"""Thin service wrapper for LangGraph image tagging.

This module provides a minimal wrapper around the LangGraph workflow
without any business logic or output modification.
"""

from typing import Dict, Any
import logging
import os

from .langgraph_integration.langgraph_service import run_langgraph_on_url

logger = logging.getLogger(__name__)


def run_image_tagger(image_url: str, mode: str = "fast") -> Dict[str, Any]:
    """Run the LangGraph image tagging pipeline.
    
    This is a thin wrapper that calls the LangGraph workflow and handles
    exceptions. It does not modify, normalize, or restructure the output.
    
    Args:
        image_url: Public URL of the product image to analyze
        mode: Processing mode - "fast" (default), "reasoning", "advanced_reasoning"
    
    Returns:
        Dict with keys:
        - 'english': English tags from LangGraph
        - 'persian': Persian tags from LangGraph
        
        On failure, returns empty dicts: {"english": {}, "persian": {}}
    """
    try:
        result = run_langgraph_on_url(image_url, mode=mode)
        return result
    except Exception as e:
        logger.error(
            "Error in LangGraph image tagging pipeline for %s (mode=%s): %s",
            image_url,
            mode,
            str(e),
            exc_info=True,
        )
        return {"english": {}, "persian": {}}
