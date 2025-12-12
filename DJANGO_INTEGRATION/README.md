# Django Integration Files for image_tagging_service

This directory contains everything needed to integrate your LangGraph image tagging pipeline into a Django REST Framework backend.

## Files Included

### 1. `tagger.py` ⭐ **MAIN FILE**
Production-ready service layer that:
- Wraps the LangGraph pipeline
- Normalizes complex entity arrays to flat Django schema
- Handles all errors gracefully (returns None values instead of exceptions)
- Provides comprehensive logging

**Copy to:** `fashion_tagger/services/tagger.py`

**Key function:**
```python
def generate_tags(image_url: str, mode: str = "fast") -> Dict[str, Optional[str]]:
    """Generate {category, color, material} from image URL"""
```

### 2. `integration_guide.md` 📖 **STEP-BY-STEP GUIDE**
Complete deployment guide with:
- 10-step setup instructions
- Architecture diagrams
- Testing examples (unit + integration)
- Logging configuration
- Production checklist
- Troubleshooting section

**Read this first** for understanding the full integration.

### 3. `views_example.py` 👀 **REFERENCE CODE**
4 different implementation examples:
1. **Main** - with mode selection via query parameter
2. **Simple** - minimal version (no mode param)
3. **Cached** - with 24-hour TTL caching
4. **Robust** - with explicit timeout + error handling

Each shows what 1-3 lines need to change in your existing `views.py`.

### 4. `quick_reference.txt` 🚀 **OPERATIONS CHEAT SHEET**
One-page reference with:
- Constraint compliance checklist (your 5 constraints verified ✓)
- Copy-paste quickstart
- Environment variables
- Function signatures
- Deployment checklist
- Troubleshooting

**Bookmark this** for quick lookups during implementation.

### 5. `import_paths_fix.py` ⚠️ **CRITICAL SETUP**
Handles the tricky part:
- Explains why relative imports break in Django
- Provides automated fix script
- Shows manual fix instructions
- Includes verification commands

**Must run this** after copying your LangGraph files.

## Quick Start

### 1. Copy Integration Files
```bash
cp tagger.py fashion_tagger/services/
cp integration_guide.md DOCS/
cp quick_reference.txt DOCS/
```

### 2. Copy LangGraph Files
```bash
mkdir -p fashion_tagger/services/langgraph_service
cp image_to_tags.py fashion_tagger/services/langgraph_service/
cp merge_results.py fashion_tagger/services/langgraph_service/
cp langgraph_service.py fashion_tagger/services/langgraph_service/
cp serpapi_search.py fashion_tagger/services/langgraph_service/
cp config.py fashion_tagger/services/langgraph_service/
cp init.py fashion_tagger/services/langgraph_service/__init__.py
cp model_client.py fashion_tagger/services/langgraph_service/
cp translate_tags.py fashion_tagger/services/langgraph_service/
```

### 3. Fix Import Paths ⚠️ **CRITICAL**
```bash
python import_paths_fix.py fix_imports("fashion_tagger/services/langgraph_service")
```
Or manually update all relative imports to absolute Django paths.

### 4. Update views.py
```python
from .services.tagger import generate_tags  # ← ADD THIS

class TagImageView(APIView):
    def post(self, request):
        image_url = request.data.get("image_url")
        tags = generate_tags(image_url)  # ← CHANGE THIS LINE
        return Response({"image_url": image_url, "tags": tags})
```

### 5. Set Environment Variable
```bash
export OPENROUTER_API_KEY=sk_xxx...
```

### 6. Test
```bash
python manage.py test
```

## What Changed

**Created:**
- ✅ `fashion_tagger/services/tagger.py` (200 lines)
- ✅ `fashion_tagger/services/langgraph_service/` (your code)

**Modified:**
- ✅ `fashion_tagger/views.py` (1 line + 1 import)
- ✅ `.env` or `settings.py` (add config)

**Untouched:**
- ✓ Authentication
- ✓ Rate limiting
- ✓ API response shape
- ✓ Project structure
- ✓ Endpoints

## Constraints Compliance

All 5 constraints verified ✓:

1. **No authentication changes** - `tagger.py` is pure service, views.py keeps auth
2. **No rate limiting changes** - All DRF middleware untouched
3. **No response shape changes** - Endpoint still returns `{"image_url": "...", "tags": {...}}`
4. **No project structure rewrites** - Only 3 new files
5. **No new endpoints** - Modified existing `POST /api/v1/tag/` only

## Support

For each file:
- **tagger.py**: See inline docstrings
- **integration_guide.md**: Read Step-by-step
- **views_example.py**: Copy relevant example
- **quick_reference.txt**: Look up details
- **import_paths_fix.py**: Run or follow manual steps

## Next Steps

1. Read `integration_guide.md` (10 steps)
2. Follow Quick Start above
3. Use `views_example.py` as reference
4. Check `quick_reference.txt` during implementation
5. Run `import_paths_fix.py` for import conversion
6. Test and deploy

**Total setup time: ~30 minutes**

Good luck! 🚀
