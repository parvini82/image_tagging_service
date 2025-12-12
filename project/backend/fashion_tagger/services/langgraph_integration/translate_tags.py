from typing import Any, Dict

from .config import TRANSLATE_MODEL
from .model_client import OpenRouterClient, make_text_part


def build_translation_prompt(data: Dict[str, Any]) -> str:
    return (
        "You are a product understanding and normalization model specialized in fashion and apparel.\n\n"
        "Input:\n"
        "- image_tags_en: structured English tags from a vision model\n"
        "  (product_type, color, material, style, etc.)\n\n"
        "Goal:\n"
        "Normalize and standardize the product tags to a consistent format.\n"
        "Focus on extracting the primary category, dominant color, and main material.\n\n"
        "Rules:\n"
        "1. Identify the primary product category from product_type.\n"
        "2. Extract the primary (most visible) color.\n"
        "3. Extract the main material/fabric if available.\n"
        "4. Output only a clean standardized JSON object.\n\n"
        f"Input data:\n{data}\n\n"
        "Output format (strict JSON only):\n"
        "{\n"
        ' "category": "category_name_or_null",\n'
        ' "color": "color_name_or_null",\n'
        ' "material": "material_name_or_null"\n'
        "}\n\n"
        "Output (valid JSON only, no explanations):"
    )


def translate_tags_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Translation node: normalize English tags to standardized format."""
    image_tags_en = state.get("image_tags_en")
    if not image_tags_en:
        raise ValueError("translate_tags_node: 'image_tags_en' is missing in state")

    client = OpenRouterClient()
    combined_input = {
        "image_tags_en": image_tags_en,
    }

    prompt = build_translation_prompt(combined_input)
    messages = [
        {
            "role": "user",
            "content": [make_text_part(prompt)],
        }
    ]

    result = client.call_json(model=TRANSLATE_MODEL, messages=messages)
    image_tags_fa = result["json"] or {}

    return {
        **state,
        "image_tags_fa": image_tags_fa,
        "translation_raw": result.get("text"),
    }
