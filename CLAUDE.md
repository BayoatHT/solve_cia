# CLAUDE.md - AI Assistant Guide

> CIA World Factbook Data Processing Toolkit (proj_004_cia v0.1.0)

## Project Overview

This is a Python package for extracting, parsing, transforming, and organizing CIA World Factbook data into structured formats. The toolkit processes raw JSON data from 269 countries/territories across 14 geographic regions into normalized, analyzable datasets.

**Key Capabilities:**
- Extract CIA World Factbook JSON data from multiple regions
- Parse unstructured text into structured formats
- Map CIA country codes to ISO 2/3 codes
- Generate product datasets by geographic categories and economic sectors
- Support multilingual translation

## Quick Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Install package in development mode
python setup.py develop

# Main entry point for data extraction
python -m proj_004_cia.b_01_extract.extract_usa_cia_to_local
```

## Project Structure

```
solve_cia/
├── setup.py                    # Package configuration
├── requirements.txt            # Dependencies (25 packages)
├── .gitignore
└── proj_004_cia/               # Main package (685 .py files, 279 JSON files)
    │
    ├── CORE INFRASTRUCTURE
    ├── __config/config.py      # Centralized configuration
    ├── __logger/logger.py      # Custom logging with levels: SUCCESS, AGENT, BUSINESS, DATA
    ├── __utils/                # Shared utilities
    │
    ├── RAW DATA
    ├── _raw_data/              # Original CIA JSON files by region (14 regions)
    │   ├── africa/, europe/, middle-east/, etc.
    │   └── world/              # Global aggregates
    │
    ├── MODULES (prefixed by function)
    ├── a_XX_*/                 # Analysis/Auxiliary (7 modules)
    ├── b_XX_*/                 # Extraction
    ├── c_XX_*/                 # Transformation/Parsing (13 categories)
    ├── d_XX_*/                 # Distribution/Deployment
    ├── e_XX_*/                 # Data Loading
    ├── x_XX_*/                 # Return/Export
    └── y_to_product/           # Product Generation (13 category outputs)
```

## Module Naming Convention

| Prefix | Purpose | Example |
|--------|---------|---------|
| `a_XX_` | Analysis/Auxiliary | `a_01_cia_to_iso/` - Code mapping |
| `b_XX_` | Extraction | `b_01_extract/` - Main extractor |
| `c_XX_` | Category parsers | `c_02_geography/` - Geography data |
| `d_XX_` | Distribution | `d_01_translate_all/` - Translation |
| `e_XX_` | Loading | `e_00_load_utils/` - Data loaders |
| `x_XX_` | Return/Export | `x_return/` - Export formatting |
| `y_to_product/` | Products | Output by category (a-m) |

## Data Categories (c_XX modules)

| Module | Category | Description |
|--------|----------|-------------|
| `c_01_intoduction/` | Introduction | Background info |
| `c_02_geography/` | Geography | Location, area, terrain, resources |
| `c_03_society/` | Society | Demographics, languages, religion |
| `c_04_environment/` | Environment | Climate, hazards |
| `c_05_government/` | Government | Political structure |
| `c_06_economy/` | Economy | GDP, trade, industries |
| `c_07_energy/` | Energy | Production, consumption |
| `c_08_communications/` | Communications | Telecom infrastructure |
| `c_09_transportation/` | Transportation | Roads, airports, ports |
| `c_10_military/` | Military | Defense statistics |
| `c_11_space/` | Space | Space programs |
| `c_12_terrorism/` | Terrorism | Threat assessments |
| `c_13_issues/` | Issues | International disputes |

## Standard Module Structure

Each category module follows this pattern:

```
c_0X_[category]/
├── __init__.py
├── helper/
│   ├── get_[category].py       # Main extraction function
│   └── utils/
│       ├── parse_*.py          # Field-specific parsers
│       └── __init__.py
└── return_[category]_data.py   # Export function
```

## Key Entry Points

| File | Purpose |
|------|---------|
| `b_01_extract/extract_usa_cia_to_local.py` | Main pipeline orchestrator |
| `c_0X_*/return_*_data.py` | Category export functions |
| `__config/config.py` | Configuration management |
| `__logger/logger.py` | Logging utilities |

## Core Utility Functions

Located in `c_00_transform_utils/`:

| Function | File | Purpose |
|----------|------|---------|
| `clean_text()` | `clean_text.py` | HTML/Unicode normalization |
| `extract_numeric_value()` | `extract_numeric_value.py` | Smart number parsing with ranges |
| `parse_list_from_string()` | `parse_list_from_string.py` | Text to array conversion |
| `parse_coordinates()` | `parse_coordinates.py` | Geographic coordinate parsing |
| `parse_text_field()` | `parse_text_field.py` | Generic text extraction |
| `parse_text_and_note()` | `parse_text_and_note.py` | Text + annotation parsing |
| `parse_percentage_data()` | `parse_percentage_data.py` | Percentage extraction |
| `extract_and_parse()` | `extract_and_parse.py` | Generic extraction framework |

## Import Patterns

```python
# Standard imports
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.__config.config import Config

# Transform utilities
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.extract_numeric_value import extract_numeric_value

# Category-specific
from proj_004_cia.c_02_geography.return_geography_data import return_geography_data
```

## Logging

The custom logger (`app_logger`) supports these levels:

| Level | Use Case |
|-------|----------|
| `DEBUG` | Performance metrics, detailed tracing |
| `INFO` | General operation flow |
| `WARNING` | Missing sections, fallback behaviors |
| `ERROR` | Parsing failures, IO errors |
| `SUCCESS` | Successful completion markers |
| `AGENT` | Agent-specific operations |
| `BUSINESS` | Business logic events |
| `DATA` | Data processing events |

```python
from proj_004_cia.__logger.logger import app_logger

app_logger.info("Processing country data")
app_logger.error("Failed to parse geography section")
```

## Configuration

Via `__config/config.py` and `.env`:

- **Environments:** Development, Production, Testing
- **Databases:** PostgreSQL (primary), SQLite (fallback)
- **AI Services:** OpenAI, Anthropic, Gemini, DeepSeek, HuggingFace
- **LLM Settings:** Model selection, temperature, token limits

## Data Flow Pipeline

```
1. RAW DATA           _raw_data/*.json (279 files, 14 regions)
       ↓
2. EXTRACTION         b_01_extract/extract_usa_cia_to_local.py
       ↓
3. CATEGORY ROUTING   c_0X_[category]/helper/get_[category].py
       ↓
4. FIELD PARSING      c_0X_[category]/helper/utils/parse_*.py
       ↓
5. NORMALIZATION      c_00_transform_utils/*.py
       ↓
6. EXPORT             c_0X_[category]/return_[category]_data.py
       ↓
7. PRODUCTS           y_to_product/[a-m]_[category]/
```

## Code Conventions

### Naming
- **Variables:** `snake_case` with descriptive names (`iso3Code`, `geo_area_total_sq_km`)
- **Functions:** `verb_noun` pattern (`parse_area_data`, `clean_text`)
- **Modules:** `prefix_number_description` (`c_02_geography`)

### Error Handling
```python
try:
    result = parse_data(raw_input)
except Exception as e:
    app_logger.error(f"Parsing failed: {e}")
    return {}  # Graceful degradation
```

### Type Hints
```python
from typing import Optional, Dict, List, Union

def parse_field(data: Dict, key: str) -> Optional[str]:
    ...
```

### Docstrings
```python
def extract_numeric_value(text: str) -> Dict:
    """
    Extract numeric values from text with range support.

    Args:
        text: Raw text containing numeric data

    Returns:
        Dict with 'value', 'min', 'max', 'unit' keys

    Examples:
        >>> extract_numeric_value("15-25 sq km")
        {'min': 15, 'max': 25, 'unit': 'sq km'}
    """
```

## Geographic Regions (14)

| Region | Directory |
|--------|-----------|
| Africa | `_raw_data/africa/` |
| Antarctica | `_raw_data/antarctica/` |
| Australia-Oceania | `_raw_data/australia-oceania/` |
| Central America & Caribbean | `_raw_data/central-america-n-caribbean/` |
| Central Asia | `_raw_data/central-asia/` |
| East & Southeast Asia | `_raw_data/east-n-southeast-asia/` |
| Europe | `_raw_data/europe/` |
| Meta (EU, etc.) | `_raw_data/meta/` |
| Middle East | `_raw_data/middle-east/` |
| North America | `_raw_data/north-america/` |
| Oceans | `_raw_data/oceans/` |
| South America | `_raw_data/south-america/` |
| South Asia | `_raw_data/south-asia/` |
| World | `_raw_data/world/` |

## Key Dependencies

| Package | Purpose |
|---------|---------|
| `pandas`, `numpy` | Data processing |
| `beautifulsoup4` | HTML parsing |
| `fuzzywuzzy` | Fuzzy string matching |
| `requests`, `httpx` | HTTP clients |
| `fastapi`, `pydantic` | API framework |
| `psycopg2` | PostgreSQL driver |
| `selenium` | Web scraping |
| `python-dotenv` | Environment variables |

## Adding a New Category Parser

1. Create module directory: `c_XX_newcategory/`
2. Add structure:
   ```
   c_XX_newcategory/
   ├── __init__.py
   ├── helper/
   │   ├── __init__.py
   │   ├── get_newcategory.py
   │   └── utils/
   │       ├── __init__.py
   │       └── parse_specific_field.py
   └── return_newcategory_data.py
   ```
3. Implement `get_newcategory()` to extract raw section
4. Add field parsers in `utils/`
5. Implement `return_newcategory_data()` for export
6. Register in main extractor

## Adding a New Field Parser

1. Create parser in appropriate `helper/utils/`:
   ```python
   # c_XX_category/helper/utils/parse_new_field.py
   from proj_004_cia.c_00_transform_utils.clean_text import clean_text

   def parse_new_field(data: dict) -> dict:
       """Parse new field from raw data."""
       raw = data.get('new_field', {})
       return {
           'value': clean_text(raw.get('text', '')),
           'note': raw.get('note')
       }
   ```
2. Import and use in `get_category.py`

## Testing

Currently no formal test framework. When adding tests:

1. Create `tests/` directory
2. Use pytest: `pip install pytest`
3. Follow naming: `test_*.py`
4. Test parsing utilities thoroughly (edge cases in CIA data)

## Common Tasks

### Process a single country
```python
from proj_004_cia.c_02_geography.return_geography_data import return_geography_data

# Load raw JSON for a country
import json
with open('proj_004_cia/_raw_data/europe/france.json') as f:
    data = json.load(f)

# Process geography section
geo_data = return_geography_data(data, 'FRA')
```

### Add ISO code mapping
```python
# a_01_cia_to_iso/utils/country_name_to_code.py
COUNTRY_MAP = {
    'new-country': {'iso2': 'XX', 'iso3': 'XXX'},
    ...
}
```

## Notes for AI Assistants

1. **Module Hierarchy:** Always respect the prefix naming system (a_, b_, c_, etc.)
2. **Graceful Errors:** Return empty dict/None rather than raising exceptions
3. **Logging:** Use `app_logger` for all output, not print statements
4. **Type Safety:** Include type hints on all new functions
5. **CIA Data Quirks:** Data often has inconsistent formatting - handle edge cases
6. **Unit Normalization:** Convert all measurements to standard units
7. **Preserve Metadata:** Keep notes, estimates, and uncertainty markers
8. **No Breaking Changes:** Maintain backward compatibility in return structures
