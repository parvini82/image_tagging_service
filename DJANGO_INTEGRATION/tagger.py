"""
Fashion image tagging service using LangGraph pipeline.

Integrates LangGraph-based vision model with Django endpoint.
Extracts category, color, material from product images.

Production-ready with graceful error handling and null-safe output.
"""

import logging
from typing import Dict, Optional, Any
import requests
from requests.exceptions import RequestException, Timeout

logger = logging.getLogger(__name__)


def _extract_scalar_value(
    entities_list: list, entity_name: str, fallback: Optional[str] = None
) -> Optional[str]:
    """
    Extract first value from entity array in LangGraph output.
    
    Expected input format (from LLM):
        [{"name": "color", "values": ["blue", "red"]}, ...]
    
    Returns first value if found, otherwise fallback (default: None).
    """
    if not isinstance(entities_list, list):
        return fallback
    
    for entity in entities_list:
        if isinstance(entity, dict) and entity.get("name") == entity_name:
            values = entity.get("values", [])
            if isinstance(values, list) and len(values) > 0:
                return values[0]
    
    return fallback


def _normalize_langgraph_output(
    langgraph_result: Dict[str, Any],
) -> Dict[str, Optional[str]]:
    """
    Normalize LangGraph output to Django-expected shape.
    
    LangGraph returns:
        {
            "english": {"entities": [...]},
            "persian": {"entities": [...]}
        }
    
    Django expects:
        {
            "category": str | None,
            "color": str | None,
            "material": str | None
        }
    
    We prioritize English tags, fallback to Persian if needed.
    """
    # Extract English tags (primary source)
    english_data = langgraph_result.get("english", {})
    english_entities = english_data.get("entities", [])
    
    # Extract Persian tags (secondary source)
    persian_data = langgraph_result.get("persian", {})
    persian_entities = persian_data.get("entities", [])
    
    # Extract values with priority: English > Persian > None
    category = (
        _extract_scalar_value(english_entities, "product_type")
        or _extract_scalar_value(persian_entities, "product_type")
        or None
    )
    
    color = (
        _extract_scalar_value(english_entities, "color")
        or _extract_scalar_value(persian_entities, "color")
        or None
    )
    
    material = (
        _extract_scalar_value(english_entities, "material")
        or _extract_scalar_value(persian_entities, "material")
        or None
    )
    
    return {
        "category": category,
        "color": color,
        "material": material,
    }


def _fetch_image(image_url: str, timeout: int = 30) -> Optional[bytes]:
    """
    Fetch image from URL with error handling.
    
    Args:
        image_url: Remote image URL
        timeout: Request timeout in seconds
    
    Returns:
        Image bytes if successful, None on failure
    """
    try:
        response = requests.get(image_url, timeout=timeout, stream=True)
        response.raise_for_status()
        
        # Limit to 50MB
        content_length = response.headers.get("content-length")
        if content_length and int(content_length) > 50 * 1024 * 1024:
            logger.warning(f"Image too large: {image_url}")
            return None
        
        return response.content
    
    except Timeout:
        logger.error(f"Image fetch timeout: {image_url}")
        return None
    
    except RequestException as e:
        logger.error(f"Image fetch failed: {image_url} - {str(e)}")
        return None
    
    except Exception as e:
        logger.error(f"Unexpected error fetching image: {image_url} - {str(e)}")
        return None


def generate_tags(image_url: str, mode: str = "fast") -> Dict[str, Optional[str]]:
    """
    Generate fashion product tags from image URL.
    
    Orchestrates the LangGraph pipeline:
    1. Fetch image from URL
    2. Run through LangGraph workflow
    3. Normalize output to Django schema
    
    Args:
        image_url: Remote image URL (must be publicly accessible)
        mode: Pipeline mode - "fast" (default), "reasoning", "advanced_reasoning"
              Controls model selection and whether to use SerpAPI
    
    Returns:
        Dict with keys: category, color, material
        Values are either strings or None (safe for database storage)
    
    Raises:
        ImportError: If langgraph is not installed
    
    Example:
        >>> tags = generate_tags("https://example.com/product.jpg")
        >>> tags
        {"category": "t-shirt", "color": "blue", "material": "cotton"}
    """
    # Import LangGraph here to avoid hard dependency if not used
    try:
        from .langgraph_service import run_langgraph_on_url
    except ImportError as e:
        logger.error("LangGraph service not available: %s", str(e))
        return {"category": None, "color": None, "material": None}
    
    # Default error response
    error_response = {"category": None, "color": None, "material": None}
    
    # Validate URL
    if not image_url or not isinstance(image_url, str):
        logger.warning("Invalid image_url provided: %s", image_url)
        return error_response
    
    try:
        # Run LangGraph pipeline with the provided URL
        # LangGraph will handle data URI conversion internally if needed
        langgraph_output = run_langgraph_on_url(image_url, mode=mode)
        
        if not langgraph_output:
            logger.warning("LangGraph returned empty output for: %s", image_url)
            return error_response
        
        # Normalize to Django schema
        normalized_tags = _normalize_langgraph_output(langgraph_output)
        
        # Log successful extraction (for monitoring)
        logger.info(
            "Tags generated successfully: %s",
            normalized_tags
        )
        
        return normalized_tags
    
    except Exception as e:
        logger.error(
            "Error generating tags for %s: %s",
            image_url,
            str(e),
            exc_info=True
        )
        return error_response
