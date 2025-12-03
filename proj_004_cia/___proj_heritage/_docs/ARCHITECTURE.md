# World Heritage Data Processing System - Architecture

## Executive Summary

This system processes UNESCO World Heritage data from a single JSON file containing **1,248 heritage sites** across **170 countries** in **5 regions**. The architecture follows the proven patterns from the CIA World Factbook toolkit but simplified for a single data source.

### Key Statistics
- **Total Sites**: 1,248
- **Countries**: 170 (ISO2 codes)
- **Regions**: 5 (Europe & North America: 580, Asia & Pacific: 305, Latin America & Caribbean: 154, Africa: 112, Arab States: 97)
- **Categories**: Cultural (972), Natural (235), Mixed (41)
- **Transboundary Sites**: 51 (spanning multiple countries)
- **Sites in Danger**: 53
- **Languages**: 6 (English, French, Spanish, Russian, Arabic, Chinese)

---

## Data Structure Analysis

### Core Attributes (37 fields per site)

#### Identity & Names (7 fields)
- `name_en`, `name_fr`, `name_es`, `name_ru`, `name_ar`, `name_zh` - Multilingual names
- `uuid` - Unique identifier

#### Descriptions (7 fields)
- `short_description_*` (6 languages) - Brief summaries
- `description_en` - Full English description
- `justification_en` - UNESCO justification text

#### Geographic Data (6 fields)
- `coordinates` - `{lon, lat}` object (1 site missing)
- `region` - "Europe and North America", "Asia and the Pacific", etc.
- `region_code` - "EUR", "ASP", "LAC", "AFR", "ARB"
- `states_names` - Array of country names
- `iso_codes` - Comma-separated ISO2 codes (e.g., "IT, FR, AT")
- `transboundary` - "True"/"False" string

#### Classification (6 fields)
- `category` - "Cultural", "Natural", "Mixed"
- `category_id` - 1 (Cultural), 2 (Natural), 3 (Mixed)
- `cultural_criteria` - "c1, c2, c3" etc. (30 unique combinations)
- `natural_criteria` - "n7, n8, n9, n10" etc. (15 unique combinations)
- `criteria_txt` - "(i)(ii)(iii)" formatted text
- `area_hectares` - Float (23 sites have null)

#### Temporal Data (4 fields)
- `date_inscribed` - Year as string (e.g., "1992")
- `secondary_dates` - "1992, 1999" (extensions/modifications)
- `danger` - "True"/"False" string
- `date_end` - Delisting date (mostly null)
- `danger_list` - Details if endangered (mostly null)

#### Images (2 fields)
- `main_image_url` - Dict with metadata (21 sites missing):
  ```json
  {
    "id": "3f533544...",
    "filename": "site_0570_0001.jpg",
    "url": "https://data.unesco.org/...",
    "format": "JPEG",
    "width": 1840,
    "height": 1232,
    "thumbnail": true,
    "exif_orientation": 1,
    "color_summary": ["rgba(...)", ...]
  }
  ```
- `images_urls` - Comma-separated string of URLs (multiple images per site)

#### Components (3 fields) - For multi-location sites
- `components_list` - String with component details
- `components_count` - Integer (1-111, transboundary sites have most)
- `id_no` - UNESCO ID number

---

## Proposed Folder Architecture

```
___proj_heritage/
│
├── _docs/                           # Documentation
│   ├── ARCHITECTURE.md              # This file
│   ├── ISO2_TO_ISO3_MAPPING.md      # Complete ISO code mapping
│   ├── DATA_DICTIONARY.md           # Field definitions and patterns
│   └── PROCESSING_NOTES.md          # Edge cases and special handling
│
├── _raw_data/                       # Original data
│   └── json/
│       └── all_world_heritage.json  # Source file (17.6MB, 1,248 sites)
│
├── __config/                        # Configuration
│   ├── __init__.py
│   ├── config.py                    # Settings (languages, paths, etc.)
│   └── iso_mapping.py               # ISO2 to ISO3 conversion dict
│
├── __utils/                         # Shared utilities
│   ├── __init__.py
│   ├── generate_site_key.py         # Slugify name_en to unique key
│   ├── clean_text.py                # Text normalization
│   ├── parse_coordinates.py         # Coordinate extraction
│   ├── parse_date.py                # Date parsing utilities
│   ├── parse_criteria.py            # Criteria string parsing
│   └── handle_null_values.py       # Null/missing data handling
│
├── a_01_load/                       # Data loading
│   ├── __init__.py
│   └── load_heritage_data.py        # Load JSON, validate structure
│
├── b_01_transform/                  # Data transformation (attribute-specific)
│   ├── __init__.py
│   │
│   ├── identity/                    # Names and identifiers
│   │   ├── __init__.py
│   │   ├── parse_names.py           # Extract all 6 language names
│   │   ├── generate_keys.py         # Create unique site keys
│   │   └── parse_identifiers.py    # UUID, id_no handling
│   │
│   ├── geographic/                  # Location data
│   │   ├── __init__.py
│   │   ├── parse_coordinates.py     # Extract lat/lon
│   │   ├── parse_countries.py       # ISO2 to ISO3 conversion
│   │   ├── parse_regions.py         # Region classification
│   │   └── handle_transboundary.py  # Multi-country sites
│   │
│   ├── descriptive/                 # Text content
│   │   ├── __init__.py
│   │   ├── parse_descriptions.py    # Short/long descriptions
│   │   └── parse_justification.py   # UNESCO justification
│   │
│   ├── classification/              # Categories and criteria
│   │   ├── __init__.py
│   │   ├── parse_category.py        # Cultural/Natural/Mixed
│   │   ├── parse_criteria.py        # Parse c1-c5, n7-n10
│   │   └── parse_area.py            # Area in hectares
│   │
│   ├── temporal/                    # Dates and status
│   │   ├── __init__.py
│   │   ├── parse_inscription_dates.py  # Primary and secondary dates
│   │   ├── parse_danger_status.py      # Danger flag and details
│   │   └── parse_delisting.py          # date_end handling
│   │
│   ├── visual/                      # Image data
│   │   ├── __init__.py
│   │   ├── parse_main_image.py      # Extract main_image_url dict
│   │   └── parse_image_gallery.py   # Parse images_urls string
│   │
│   └── components/                  # Multi-location sites
│       ├── __init__.py
│       ├── parse_components.py      # Extract component details
│       └── count_components.py      # Component counting
│
├── c_01_normalize/                  # Data normalization
│   ├── __init__.py
│   ├── normalize_site.py            # Normalize single site data
│   └── validate_site.py             # Data validation
│
├── d_01_aggregate/                  # Data aggregation
│   ├── __init__.py
│   ├── by_country.py                # Group sites by country (ISO3)
│   ├── by_region.py                 # Group sites by region
│   ├── by_category.py               # Group by Cultural/Natural/Mixed
│   ├── by_criteria.py               # Group by specific criteria
│   └── by_danger_status.py          # Group endangered sites
│
├── e_01_extract/                    # Main extraction pipeline
│   ├── __init__.py
│   └── extract_all_sites.py         # Orchestrator script
│
├── x_return/                        # Output generation
│   ├── __init__.py
│   ├── return_site_data.py          # Single site complete data
│   ├── return_country_sites.py      # All sites for a country
│   ├── return_region_sites.py       # All sites in a region
│   └── return_all_sites.py          # Complete dataset output
│
└── y_to_product/                    # Final data products
    ├── __init__.py
    ├── sites_by_key/                # Individual site files
    │   ├── README.md
    │   └── {site_key}.json          # One file per site
    │
    ├── sites_by_country/            # Country-grouped data
    │   ├── README.md
    │   └── {iso3_code}.json         # All sites per country
    │
    ├── sites_by_region/             # Region-grouped data
    │   ├── README.md
    │   ├── europe_north_america.json
    │   ├── asia_pacific.json
    │   ├── latin_america_caribbean.json
    │   ├── africa.json
    │   └── arab_states.json
    │
    ├── sites_by_category/           # Category-grouped data
    │   ├── README.md
    │   ├── cultural.json
    │   ├── natural.json
    │   └── mixed.json
    │
    ├── special_collections/         # Curated collections
    │   ├── README.md
    │   ├── transboundary_sites.json
    │   ├── endangered_sites.json
    │   └── delisted_sites.json
    │
    └── complete/                    # Full dataset
        ├── README.md
        └── all_heritage_sites.json  # Complete normalized data
```

---

## Data Processing Pipeline

### Phase 1: Load & Validate
```
a_01_load/load_heritage_data.py
  ↓
- Load JSON file
- Validate structure (1,248 sites expected)
- Check for required fields
- Log any anomalies
```

### Phase 2: Transform by Attribute
```
b_01_transform/{category}/parse_*.py
  ↓
Each parser handles ONE attribute type:

- identity/parse_names.py          → Extract all 6 language names
- identity/generate_keys.py        → Create unique site key (slugified name_en)
- geographic/parse_countries.py    → Convert ISO2 to ISO3 codes
- geographic/parse_coordinates.py  → Extract lat/lon, handle missing (1 site)
- temporal/parse_inscription_dates → Parse inscription dates
- visual/parse_main_image.py       → Extract image metadata
- etc.
```

### Phase 3: Normalize
```
c_01_normalize/normalize_site.py
  ↓
- Combine all parsed attributes
- Apply consistent structure
- Handle null values (23 missing area, 21 missing images)
- Validate against schema
```

### Phase 4: Aggregate
```
d_01_aggregate/{aggregation_type}.py
  ↓
- by_country.py    → Group by ISO3 code
- by_region.py     → Group by UNESCO region
- by_category.py   → Group Cultural/Natural/Mixed
- by_criteria.py   → Group by specific criteria
```

### Phase 5: Export
```
x_return/return_*.py
  ↓
Generate outputs:
- Individual site JSON (1,248 files)
- Country aggregations (170 files)
- Region aggregations (5 files)
- Category aggregations (3 files)
- Special collections (transboundary, endangered, etc.)
```

---

## Key Design Decisions

### 1. Site Key Generation
**Strategy**: Slugify `name_en` with underscores
```python
# Example: "Butrint" → "butrint"
# Example: "Al Qal'a of Beni Hammad" → "al_qala_of_beni_hammad"
# Example: "Historic Centre of Prague" → "historic_centre_of_prague"

from slugify import slugify

def generate_site_key(name_en: str) -> str:
    """Generate unique key from English name."""
    return slugify(name_en, separator='_', lowercase=True)
```

**Collision Handling**: If duplicate keys exist, append `_{iso3}` or `_{id_no}`

### 2. ISO2 to ISO3 Mapping
**Challenge**: UNESCO uses ISO2, system uses ISO3

**Solution**: Complete mapping dictionary in `__config/iso_mapping.py`
```python
ISO2_TO_ISO3 = {
    'AD': 'AND',  # Andorra
    'AE': 'ARE',  # United Arab Emirates
    'AF': 'AFG',  # Afghanistan
    # ... all 170 codes
}
```

### 3. Transboundary Sites
**Challenge**: 51 sites span multiple countries

**Strategy**:
- Primary representation: Store under ALL countries
- Metadata flag: `"is_transboundary": True`
- Country list: `"countries": ["FRA", "ITA", "DEU"]` (ISO3)
- Components: Parse `components_list` to extract locations

**Example Output**:
```json
{
  "site_key": "prehistoric_pile_dwellings_around_the_alps",
  "is_transboundary": true,
  "countries": ["ITA", "FRA", "AUT", "SVN", "CHE", "DEU"],
  "components": {
    "count": 111,
    "locations": [
      {
        "name": "See",
        "ref": "1363-061",
        "coordinates": {"lat": 47.803881, "lon": 13.449282}
      },
      // ... 110 more
    ]
  }
}
```

### 4. Image Handling
**main_image_url**: Dictionary structure (keep as-is)
```json
{
  "main_image": {
    "url": "https://data.unesco.org/...",
    "filename": "site_0570_0001.jpg",
    "dimensions": {"width": 1840, "height": 1232},
    "format": "JPEG",
    "has_thumbnail": true,
    "color_palette": ["rgba(239, 232, 235, 1.00)", ...]
  }
}
```

**images_urls**: Parse comma-separated string to array
```json
{
  "image_gallery": [
    "https://whc.unesco.org/document/111183/site_0570_0001.jpg",
    "https://whc.unesco.org/document/111185/site_0570_0002.jpg",
    // ... more URLs
  ],
  "gallery_count": 50
}
```

### 5. Criteria Parsing
**Cultural**: c1, c2, c3, c4, c5 (30 combinations)
**Natural**: n7, n8, n9, n10 (15 combinations)

**Input**: `"cultural_criteria": "c1, c2, c3"`
**Output**:
```json
{
  "criteria": {
    "cultural": [1, 2, 3],
    "natural": [],
    "display": "(i)(ii)(iii)",
    "count": 3
  }
}
```

### 6. Null Value Handling
**Missing area_hectares** (23 sites): `null` → `{"value": null, "note": "not_reported"}`
**Missing coordinates** (1 site): `null` → `{"lat": null, "lon": null, "note": "not_available"}`
**Missing main_image_url** (21 sites): `null` → `{"url": null, "note": "no_image"}`

### 7. Nested Dictionaries Over Arrays
**User Preference**: Dictionaries for web product ingestion

**Example - Countries**:
```json
// AVOID (array)
"countries": ["FRA", "DEU", "ITA"]

// PREFER (nested dict)
"countries": {
  "FRA": {
    "name": "France",
    "iso2": "FR",
    "iso3": "FRA"
  },
  "DEU": {
    "name": "Germany",
    "iso2": "DE",
    "iso3": "DEU"
  }
}
```

---

## Attribute-Specific Parsers

Each parser is a standalone module responsible for ONE attribute type:

| Parser Module | Input Field(s) | Output Structure |
|---------------|---------------|------------------|
| `identity/parse_names.py` | `name_*` | `{"en": "...", "fr": "...", ...}` |
| `identity/generate_keys.py` | `name_en` | `"site_key": "..."` |
| `geographic/parse_countries.py` | `iso_codes`, `states_names` | `{"countries": {...}}` |
| `geographic/parse_coordinates.py` | `coordinates` | `{"latitude": X, "longitude": Y}` |
| `geographic/parse_regions.py` | `region`, `region_code` | `{"region": {...}}` |
| `descriptive/parse_descriptions.py` | `*_description_*` | `{"descriptions": {...}}` |
| `classification/parse_category.py` | `category`, `category_id` | `{"category": {...}}` |
| `classification/parse_criteria.py` | `*_criteria`, `criteria_txt` | `{"criteria": {...}}` |
| `classification/parse_area.py` | `area_hectares` | `{"area": {...}}` |
| `temporal/parse_inscription_dates.py` | `date_inscribed`, `secondary_dates` | `{"inscription": {...}}` |
| `temporal/parse_danger_status.py` | `danger`, `danger_list` | `{"danger_status": {...}}` |
| `visual/parse_main_image.py` | `main_image_url` | `{"main_image": {...}}` |
| `visual/parse_image_gallery.py` | `images_urls` | `{"image_gallery": [...]}` |
| `components/parse_components.py` | `components_list` | `{"components": {...}}` |

---

## Output Structure (Normalized Site)

```json
{
  "site_key": "butrint",
  "uuid": "1e6988b2-e175-509e-9e43-943ffeced51a",
  "unesco_id": "570",

  "names": {
    "en": "Butrint",
    "fr": "Butrint",
    "es": "Butrinto",
    "ru": "Древний город Бутринт",
    "ar": "بوترنت",
    "zh": "布特林特"
  },

  "descriptions": {
    "short": {
      "en": "Inhabited since prehistoric times...",
      "fr": "Habité depuis les temps préhistoriques...",
      // ... other languages
    },
    "full": "Inhabited since prehistoric times...",
    "justification": "Brief synthesis Butrint, located..."
  },

  "geography": {
    "coordinates": {
      "latitude": 39.745732,
      "longitude": 20.02095
    },
    "countries": {
      "ALB": {
        "name": "Albania",
        "iso2": "AL",
        "iso3": "ALB"
      }
    },
    "region": {
      "name": "Europe and North America",
      "code": "EUR"
    },
    "is_transboundary": false
  },

  "classification": {
    "category": {
      "name": "Cultural",
      "id": 1
    },
    "criteria": {
      "cultural": [3],
      "natural": [],
      "display": "(iii)",
      "count": 1
    },
    "area": {
      "hectares": null,
      "note": "not_reported"
    }
  },

  "temporal": {
    "inscription": {
      "primary_date": 1992,
      "secondary_dates": [1992, 1999],
      "all_dates": "1992, 1999"
    },
    "danger_status": {
      "is_endangered": false,
      "details": null,
      "date_end": null
    }
  },

  "visual": {
    "main_image": {
      "url": "https://data.unesco.org/api/explore/v2.1/catalog/datasets/whc001/files/3f533544...",
      "filename": "site_0570_0001.jpg",
      "dimensions": {
        "width": 1840,
        "height": 1232
      },
      "format": "JPEG",
      "has_thumbnail": true,
      "color_palette": [
        "rgba(239, 232, 235, 1.00)",
        "rgba(144, 147, 141, 1.00)",
        "rgba(79, 98, 68, 1.00)"
      ]
    },
    "image_gallery": [
      "https://whc.unesco.org/document/111183/site_0570_0001.jpg",
      "https://whc.unesco.org/document/111185/site_0570_0002.jpg"
      // ... more URLs
    ],
    "gallery_count": 50
  },

  "components": {
    "count": 1,
    "locations": [
      {
        "name": "Butrint",
        "ref": "570ter",
        "coordinates": {
          "latitude": 39.745732,
          "longitude": 20.02095
        }
      }
    ]
  }
}
```

---

## Special Collections

### 1. Transboundary Sites (51 total)
**File**: `y_to_product/special_collections/transboundary_sites.json`

**Structure**:
```json
{
  "collection_name": "Transboundary World Heritage Sites",
  "total_sites": 51,
  "sites": {
    "prehistoric_pile_dwellings_around_the_alps": {
      "countries_count": 6,
      "countries": ["ITA", "FRA", "AUT", "SVN", "CHE", "DEU"],
      "components_count": 111,
      // ... full site data
    }
  }
}
```

### 2. Endangered Sites (53 total)
**File**: `y_to_product/special_collections/endangered_sites.json`

### 3. Sites by Country (170 files)
**File Pattern**: `y_to_product/sites_by_country/{iso3}.json`

**Example - FRA.json**:
```json
{
  "country": {
    "name": "France",
    "iso2": "FR",
    "iso3": "FRA"
  },
  "total_sites": 52,
  "sites_by_category": {
    "cultural": 44,
    "natural": 6,
    "mixed": 2
  },
  "sites": {
    "palace_and_park_of_versailles": { /* full data */ },
    "mont_saint_michel": { /* full data */ }
    // ... all French sites
  }
}
```

---

## ISO2 to ISO3 Mapping

**Location**: `__config/iso_mapping.py`

**Complete mapping for all 170 countries** will be in a separate document (`ISO2_TO_ISO3_MAPPING.md`).

Sample structure:
```python
ISO2_TO_ISO3 = {
    'AL': 'ALB',  # Albania
    'DZ': 'DZA',  # Algeria
    'FR': 'FRA',  # France
    'IT': 'ITA',  # Italy
    'DE': 'DEU',  # Germany
    'CH': 'CHE',  # Switzerland
    'AT': 'AUT',  # Austria
    # ... 163 more
}

# Reverse mapping for lookups
ISO3_TO_ISO2 = {v: k for k, v in ISO2_TO_ISO3.items()}

# Country names mapping
ISO3_TO_NAME = {
    'ALB': 'Albania',
    'DZA': 'Algeria',
    # ... all countries
}
```

---

## Edge Cases & Special Handling

### 1. Duplicate Keys
If `slugify(name_en)` produces duplicates:
```python
# First occurrence: "historic_centre"
# Second occurrence: "historic_centre_fra" (append ISO3 of first country)
# Third occurrence: "historic_centre_570" (append UNESCO id_no)
```

### 2. Components Parsing
**Input** (string): `{name: See , ref: 1363-061, latitude: 47.803881, longitude: 13.449282}, {name: Riesi, ...}`

**Strategy**:
- Split by `}, {`
- Parse each component as key-value pairs
- Extract name, ref, latitude, longitude
- Handle malformed data gracefully

### 3. Image URLs Parsing
**Input** (string): `"https://whc.unesco.org/..., https://whc.unesco.org/..."`

**Strategy**:
- Split by `, `
- Strip whitespace
- Validate URLs
- Return array

### 4. Secondary Dates
**Input**: `"1992, 1999"`

**Strategy**:
- Split by `, `
- Parse each as integer year
- Return sorted array: `[1992, 1999]`

---

## Implementation Phases

### Phase 1: Foundation (First)
1. Create folder structure
2. Implement `__config/iso_mapping.py` (complete ISO2→ISO3 map)
3. Implement `__utils/` utilities
4. Implement `a_01_load/` data loader

### Phase 2: Attribute Parsers (Core)
5. Implement all `b_01_transform/{category}/` parsers
6. One parser per attribute type
7. Test each parser independently

### Phase 3: Normalization (Integration)
8. Implement `c_01_normalize/` to combine all parsed data
9. Implement validation

### Phase 4: Aggregation (Organization)
10. Implement all `d_01_aggregate/` grouping functions
11. Test aggregations

### Phase 5: Export & Products (Output)
12. Implement `x_return/` export functions
13. Generate `y_to_product/` data files
14. Validate all 1,248 site files

---

## Testing Strategy

### Unit Tests (Per Parser)
```python
# Test: b_01_transform/identity/parse_names.py
def test_parse_names():
    site = {"name_en": "Butrint", "name_fr": "Butrint", ...}
    result = parse_names(site)
    assert result["names"]["en"] == "Butrint"
    assert len(result["names"]) == 6  # All languages
```

### Integration Tests
```python
# Test: Complete pipeline for single site
def test_full_site_processing():
    raw_site = load_raw_site("butrint")
    normalized = normalize_site(raw_site)
    assert "site_key" in normalized
    assert normalized["geography"]["countries"]["ALB"]
```

### Validation Tests
```python
# Test: All 1,248 sites process successfully
def test_all_sites():
    sites = load_heritage_data()
    for site in sites:
        normalized = normalize_site(site)
        assert validate_site(normalized) == True
```

---

## Success Criteria

✅ **Data Integrity**
- All 1,248 sites processed without errors
- All ISO2 codes mapped to ISO3 (170 countries)
- All 51 transboundary sites correctly represented
- All null values handled gracefully

✅ **Functionality**
- `get_site_by_key("butrint")` returns complete site data
- `get_sites_by_country("FRA")` returns all 52+ French sites
- `get_sites_by_region("Europe and North America")` returns 580 sites
- `get_endangered_sites()` returns 53 sites

✅ **Output Format**
- All outputs use nested dictionaries (not arrays where possible)
- All country references use ISO3 codes
- All images parsed correctly
- All multilingual fields preserved

✅ **Performance**
- Full dataset processing < 5 minutes
- Individual site lookup < 1 second
- Country aggregation < 2 seconds

---

## Dependencies

**Core**:
- `python-slugify` - Site key generation
- `pydantic` - Data validation (optional)

**Already Available** (from CIA project):
- `json` - Data loading
- Standard library utilities

**Minimal New Dependencies**: This system reuses most CIA project infrastructure.

---

## Next Steps

1. **Review this architecture** with user
2. Create `ISO2_TO_ISO3_MAPPING.md` (complete mapping)
3. Create `DATA_DICTIONARY.md` (field definitions)
4. Begin implementation (Phase 1: Foundation)
