# World Heritage Data Dictionary

Complete field definitions, patterns, and edge cases for all 37 attributes in the UNESCO World Heritage dataset.

---

## Field Summary

| Category | Fields | Count |
|----------|--------|-------|
| **Identity & Names** | `uuid`, `id_no`, `name_*` (6 languages) | 8 |
| **Descriptions** | `*_description_*` (6 languages), `description_en`, `justification_en` | 14 |
| **Geographic** | `coordinates`, `region`, `region_code`, `states_names`, `iso_codes`, `transboundary` | 6 |
| **Classification** | `category`, `category_id`, `*_criteria`, `criteria_txt`, `area_hectares` | 6 |
| **Temporal** | `date_inscribed`, `secondary_dates`, `danger`, `danger_list`, `date_end` | 5 |
| **Visual** | `main_image_url`, `images_urls` | 2 |
| **Components** | `components_list`, `components_count` | 2 |
| **TOTAL** | | **37** |

---

## Identity & Names (8 fields)

### `uuid`
**Type**: String (UUID format)
**Example**: `"1e6988b2-e175-509e-9e43-943ffeced51a"`
**Nullable**: No
**Description**: Unique identifier for the site

**Pattern**: Standard UUID v4 format (8-4-4-4-12 hex characters)

**Usage**:
```python
# Primary key for database storage
# Globally unique across all heritage sites
```

---

### `id_no`
**Type**: String (numeric)
**Example**: `"570"`, `"1363"`
**Nullable**: No
**Description**: UNESCO World Heritage Site ID number

**Pattern**: 1-4 digit number as string

**Usage**:
```python
# Official UNESCO reference number
# Used in component refs (e.g., "1363-061")
# Useful for UNESCO API queries
```

---

### `name_en`, `name_fr`, `name_es`, `name_ru`, `name_ar`, `name_zh`
**Type**: String
**Languages**: English, French, Spanish, Russian, Arabic, Chinese
**Nullable**: No (all 6 languages always present)
**Description**: Official site name in 6 languages

**Examples**:
```json
{
  "name_en": "Butrint",
  "name_fr": "Butrint",
  "name_es": "Butrinto",
  "name_ru": "Древний город Бутринт",
  "name_ar": "بوترنت",
  "name_zh": "布特林特"
}
```

**Special Cases**:
- Sometimes names are identical across languages (e.g., "Butrint" in EN/FR)
- Chinese/Arabic/Russian use native scripts
- Names may include special characters, apostrophes, hyphens

**Usage**:
```python
# Primary key generation: use name_en
# Multilingual display: use appropriate language field
# Search/indexing: index all languages
```

---

## Descriptions (14 fields)

### `short_description_en`, `short_description_fr`, `short_description_es`, `short_description_ru`, `short_description_ar`, `short_description_zh`
**Type**: String (paragraph)
**Languages**: 6 languages
**Length**: 100-500 characters typically
**Nullable**: No
**Description**: Brief summary of the site

**Example**:
```json
{
  "short_description_en": "Inhabited since prehistoric times, Butrint has been the site of a Greek colony, a Roman city and a bishopric. Following a period of prosperity under Byzantine administration, then a brief occupation by the Venetians, the city was abandoned in the late Middle Ages after marshes formed in the area. The present archaeological site is a repository of ruins representing each period in the city's development."
}
```

**Usage**:
- Card previews
- Summary displays
- SEO meta descriptions

---

### `description_en`
**Type**: String (long text)
**Length**: Same as `short_description_en` in most cases
**Nullable**: No
**Description**: Full English description (often identical to short_description_en)

**Note**: In the current dataset, this field is typically identical to `short_description_en`. Future versions may have expanded descriptions.

---

### `justification_en`
**Type**: String (very long text)
**Length**: 1000-5000+ characters
**Nullable**: No
**Description**: Detailed UNESCO justification for inscription

**Structure**: Contains multiple sections:
- "Brief synthesis" - Overview
- "Criterion (i), (ii), etc." - Criteria justifications
- "Integrity" - Site integrity assessment
- "Authenticity" - Authenticity assessment
- "Protection and management requirements" - Conservation details

**Example**:
```
"Brief synthesis Butrint, located in the south of Albania approximately 20km from the modern city of Saranda, has a special atmosphere created by a combination of archaeology, monuments and nature in the Mediterranean...

Criterion (iii): The evolution of the natural environment of Butrint led to the abandonment of the city at the end of the Middle Ages...

Integrity The property is of sufficient size (200 ha) to include a significant proportion of the attributes...

Authenticity The authenticity of the World Heritage property Butrint is related to its excellent preservation...

Protection and management requirements Butrint National Park was inscribed on the National Heritage List..."
```

**Usage**:
- Detailed site pages
- Research and documentation
- Educational materials

**Parsing Strategy**:
```python
def parse_justification(text):
    sections = {
        'synthesis': extract_section(text, 'Brief synthesis', 'Criterion'),
        'criteria': extract_criteria_sections(text),
        'integrity': extract_section(text, 'Integrity', 'Authenticity'),
        'authenticity': extract_section(text, 'Authenticity', 'Protection'),
        'protection': extract_section(text, 'Protection and management')
    }
    return sections
```

---

## Geographic (6 fields)

### `coordinates`
**Type**: Object `{lon: float, lat: float}`
**Nullable**: Yes (1 site missing)
**Description**: Geographic coordinates of the site

**Example**:
```json
{
  "coordinates": {
    "lon": 20.02095,
    "lat": 39.745732
  }
}
```

**Range**:
- Latitude: -90 to +90
- Longitude: -180 to +180

**Edge Cases**:
- 1 site has `null` coordinates
- Transboundary sites use centroid or primary location

**Usage**:
```python
# Map display
# Proximity searches
# Geographic clustering

# Handle missing coordinates
coords = site.get('coordinates')
if coords:
    lat, lon = coords['lat'], coords['lon']
else:
    # Fallback: use country centroid or skip mapping
```

---

### `region`
**Type**: String (enumerated)
**Values**: 5 possible values
**Nullable**: No
**Description**: UNESCO geographic region

**Valid Values**:
```python
REGIONS = [
    "Europe and North America",
    "Asia and the Pacific",
    "Latin America and the Caribbean",
    "Africa",
    "Arab States"
]
```

**Distribution**:
- Europe and North America: 580 sites
- Asia and the Pacific: 305 sites
- Latin America and the Caribbean: 154 sites
- Africa: 112 sites
- Arab States: 97 sites

---

### `region_code`
**Type**: String (3-letter code)
**Nullable**: No
**Description**: Region abbreviation

**Mapping**:
```python
REGION_CODES = {
    'EUR': 'Europe and North America',
    'ASP': 'Asia and the Pacific',
    'LAC': 'Latin America and the Caribbean',
    'AFR': 'Africa',
    'ARB': 'Arab States'
}
```

---

### `states_names`
**Type**: Array of strings
**Nullable**: No
**Description**: List of country names

**Examples**:
```json
// Single country
"states_names": ["Albania"]

// Transboundary
"states_names": ["Italy", "France", "Austria", "Slovenia", "Switzerland", "Germany"]
```

**Notes**:
- Uses full English country names
- Order may vary
- Count matches number of ISO2 codes

---

### `iso_codes`
**Type**: String (comma-separated ISO2 codes)
**Nullable**: No
**Description**: Country codes (ISO 3166-1 alpha-2)

**Examples**:
```json
// Single country
"iso_codes": "AL"

// Transboundary
"iso_codes": "IT, FR, AT, SI, CH, DE"
```

**Pattern**: `^[A-Z]{2}(,\s*[A-Z]{2})*$`

**Usage**:
```python
# Parse to list
iso2_list = [code.strip() for code in site['iso_codes'].split(',')]

# Convert to ISO3
from iso_mapping import ISO2_TO_ISO3
iso3_list = [ISO2_TO_ISO3[code] for code in iso2_list]
```

---

### `transboundary`
**Type**: String (boolean as string)
**Values**: `"True"` or `"False"`
**Nullable**: No
**Description**: Whether site spans multiple countries

**Distribution**:
- `"True"`: 51 sites
- `"False"`: 1,197 sites

**Usage**:
```python
# Convert to boolean
is_transboundary = site['transboundary'] == 'True'

# Filter transboundary sites
transboundary_sites = [s for s in data if s['transboundary'] == 'True']
```

---

## Classification (6 fields)

### `category`
**Type**: String (enumerated)
**Values**: 3 possible values
**Nullable**: No
**Description**: Heritage site category

**Valid Values**:
```python
CATEGORIES = ['Cultural', 'Natural', 'Mixed']
```

**Distribution**:
- Cultural: 972 sites (77.9%)
- Natural: 235 sites (18.8%)
- Mixed: 41 sites (3.3%)

---

### `category_id`
**Type**: Integer
**Values**: 1, 2, or 3
**Nullable**: No
**Description**: Numeric category identifier

**Mapping**:
```python
CATEGORY_IDS = {
    1: 'Cultural',
    2: 'Natural',
    3: 'Mixed'
}
```

---

### `cultural_criteria`
**Type**: String (comma-separated codes)
**Nullable**: Yes (null for Natural sites)
**Description**: Cultural criteria met (i-vi)

**Format**: `"c1, c2, c3"` etc.

**Valid Criteria**:
- c1 = Criterion (i): Masterpiece of human creative genius
- c2 = Criterion (ii): Interchange of human values
- c3 = Criterion (iii): Testimony to cultural tradition
- c4 = Criterion (iv): Significant stage in human history
- c5 = Criterion (v): Traditional human settlement
- c6 = Criterion (vi): Associated with events or traditions

**Combinations**: 30 unique combinations in dataset

**Examples**:
```json
"cultural_criteria": "c3"
"cultural_criteria": "c1, c2, c3"
"cultural_criteria": "c1, c2, c3, c4, c5"
"cultural_criteria": null  // Natural sites
```

---

### `natural_criteria`
**Type**: String (comma-separated codes)
**Nullable**: Yes (null for Cultural sites)
**Description**: Natural criteria met (vii-x)

**Format**: `"n7, n8"` etc.

**Valid Criteria**:
- n7 = Criterion (vii): Natural beauty/phenomena
- n8 = Criterion (viii): Geological/geomorphic features
- n9 = Criterion (ix): Ecological processes
- n10 = Criterion (x): Biodiversity/species conservation

**Combinations**: 15 unique combinations in dataset

**Examples**:
```json
"natural_criteria": "n7, n8, n9, n10"
"natural_criteria": "n7, n9"
"natural_criteria": null  // Cultural sites
```

---

### `criteria_txt`
**Type**: String (Roman numerals)
**Nullable**: No
**Description**: Display format for criteria

**Format**: `"(i)(ii)(iii)"` or `"(vii)(viii)"` or `"(iii)(vii)(ix)"`

**Examples**:
```json
"criteria_txt": "(iii)"           // Cultural only
"criteria_txt": "(vii)(viii)(x)"  // Natural only
"criteria_txt": "(ii)(iii)(ix)"   // Mixed
```

**Mapping**:
```python
CRITERIA_MAPPING = {
    'c1': '(i)',   'c2': '(ii)',  'c3': '(iii)',
    'c4': '(iv)',  'c5': '(v)',   'c6': '(vi)',
    'n7': '(vii)', 'n8': '(viii)', 'n9': '(ix)', 'n10': '(x)'
}
```

---

### `area_hectares`
**Type**: Float or null
**Nullable**: Yes (23 sites missing)
**Description**: Site area in hectares

**Examples**:
```json
"area_hectares": 150.0
"area_hectares": 6641000.0  // Large natural sites
"area_hectares": null       // 23 sites
```

**Range**: 0.01 to 6,641,000 hectares (massive variation)

**Usage**:
```python
# Handle null values
area = site.get('area_hectares')
if area:
    formatted = f"{area:,.0f} ha"
else:
    formatted = "Not reported"

# Convert to other units
if area:
    sq_km = area / 100
    sq_mi = area / 247.105
```

---

## Temporal (5 fields)

### `date_inscribed`
**Type**: String (year)
**Format**: `"YYYY"`
**Nullable**: No
**Description**: Year of UNESCO inscription

**Range**: 1978-2024 (approximately)

**Examples**:
```json
"date_inscribed": "1992"
"date_inscribed": "2015"
```

**Usage**:
```python
# Convert to integer
year = int(site['date_inscribed'])

# Calculate age
from datetime import datetime
age = datetime.now().year - year
```

---

### `secondary_dates`
**Type**: String (comma-separated years)
**Nullable**: No (but may be empty string)
**Description**: Inscription and extension dates

**Format**: `"YYYY, YYYY, YYYY"`

**Examples**:
```json
"secondary_dates": "1992"           // Single date (same as primary)
"secondary_dates": "1992, 1999"     // Extended in 1999
"secondary_dates": "1980, 1992, 2005"  // Multiple extensions
"secondary_dates": ""               // Some sites (empty)
```

**Usage**:
```python
# Parse to list
if site['secondary_dates']:
    dates = [int(d.strip()) for d in site['secondary_dates'].split(',')]
    inscription_date = min(dates)
    extension_dates = [d for d in dates if d > inscription_date]
```

---

### `danger`
**Type**: String (boolean as string)
**Values**: `"True"` or `"False"`
**Nullable**: No
**Description**: Whether site is on Danger List

**Distribution**:
- `"True"`: 53 sites (4.2%)
- `"False"`: 1,195 sites (95.8%)

**Usage**:
```python
# Convert to boolean
is_endangered = site['danger'] == 'True'

# Filter endangered sites
endangered = [s for s in data if s['danger'] == 'True']
```

---

### `danger_list`
**Type**: String or null
**Nullable**: Yes (mostly null)
**Description**: Details if/when added to Danger List

**Examples**:
```json
"danger_list": null  // Most sites
"danger_list": "Added to Danger List in 2007"  // Endangered sites
```

**Note**: Only populated for sites where `danger == "True"`

---

### `date_end`
**Type**: String (year) or null
**Nullable**: Yes (mostly null)
**Description**: Delisting date (if removed from World Heritage List)

**Examples**:
```json
"date_end": null      // Active sites (1,246+)
"date_end": "2009"    // Delisted sites (very rare)
```

**Note**: Only 1-2 sites have been delisted in UNESCO history (e.g., Dresden Elbe Valley in 2009)

---

## Visual (2 fields)

### `main_image_url`
**Type**: Object or null
**Nullable**: Yes (21 sites missing)
**Description**: Primary image with metadata

**Structure**:
```json
{
  "main_image_url": {
    "id": "3f533544d28985de4119e2761ca84191",
    "filename": "site_0570_0001.jpg",
    "url": "https://data.unesco.org/api/explore/v2.1/catalog/datasets/whc001/files/3f533544d28985de4119e2761ca84191",
    "format": "JPEG",
    "width": 1840,
    "height": 1232,
    "thumbnail": true,
    "exif_orientation": 1,
    "color_summary": [
      "rgba(239, 232, 235, 1.00)",
      "rgba(144, 147, 141, 1.00)",
      "rgba(79, 98, 68, 1.00)"
    ]
  }
}
```

**Fields**:
- `id`: Unique file identifier (hash)
- `filename`: Original filename pattern: `site_{id_no}_0001.jpg`
- `url`: Full URL to image file
- `format`: Image format (JPEG, PNG)
- `width`, `height`: Dimensions in pixels
- `thumbnail`: Boolean (always true in dataset)
- `exif_orientation`: EXIF orientation value (usually 1)
- `color_summary`: Array of dominant colors (3-5 colors)

**Edge Cases**:
- 21 sites have `null` main_image_url
- Color summary may have 3-5 colors

**Usage**:
```python
# Display image
main_img = site.get('main_image_url')
if main_img:
    img_url = main_img['url']
    dimensions = f"{main_img['width']}x{main_img['height']}"

    # Generate srcset for responsive images
    # Use color_summary for placeholders
    placeholder_color = main_img['color_summary'][0]
```

---

### `images_urls`
**Type**: String (comma-separated URLs)
**Nullable**: No (but may be empty)
**Description**: Gallery of all site images

**Format**: Long comma-separated list of URLs

**Example**:
```json
"images_urls": "https://whc.unesco.org/document/111183/site_0570_0001.jpg, https://whc.unesco.org/document/111185/site_0570_0002.jpg, https://whc.unesco.org/document/111187/site_0570_0003.jpg, ..."
```

**Characteristics**:
- Can contain 1-100+ URLs
- Pattern: `site_{id_no}_{seq}.jpg`
- Sequential numbering (0001, 0002, etc.)

**Usage**:
```python
# Parse to array
if site['images_urls']:
    gallery = [url.strip() for url in site['images_urls'].split(',')]
    gallery_count = len(gallery)

    # First image usually matches main_image_url
    first_image = gallery[0]
else:
    gallery = []
```

---

## Components (2 fields)

### `components_count`
**Type**: Integer
**Range**: 1 to 111
**Nullable**: No
**Description**: Number of separate locations/components

**Distribution**:
- Most sites: 1 component (single location)
- Transboundary sites: Often 10-111 components
- Serial sites: Multiple components even if not transboundary

**Usage**:
```python
# Identify multi-component sites
is_serial = site['components_count'] > 1

# Largest: "Prehistoric Pile Dwellings around the Alps" with 111 components
```

---

### `components_list`
**Type**: String (structured text)
**Nullable**: No
**Description**: Details of each component location

**Format**: Pseudo-JSON structure in string format
```
{name: Value, ref: Value, latitude: Value, longitude: Value}, {name: Value, ...}
```

**Example**:
```json
"components_list": "{name: Butrint, ref: 570ter, latitude: 39.745732, longitude: 20.02095}"
```

**Multi-component Example**:
```json
"components_list": "{name: See , ref: 1363-061, latitude: 47.803881, longitude: 13.449282}, {name: Riesi, ref: 1363-002, latitude: 47.317, longitude: 8.201}, {name: Port , ref: 1363-015, latitude: 46.268209, longitude: 6.210487}, ..."
```

**Parsing Strategy**:
```python
import re

def parse_components(components_str):
    """Parse component string to structured list."""
    # Split by }, {
    parts = components_str.split('}, {')

    components = []
    for part in parts:
        # Clean up braces
        part = part.strip('{}')

        # Parse key-value pairs
        component = {}
        for match in re.finditer(r'(\w+):\s*([^,}]+)', part):
            key, value = match.groups()
            value = value.strip()

            # Convert numeric values
            if key in ['latitude', 'longitude']:
                try:
                    value = float(value)
                except:
                    value = None

            component[key] = value

        if component:
            components.append(component)

    return components

# Example result:
[
    {
        'name': 'See',
        'ref': '1363-061',
        'latitude': 47.803881,
        'longitude': 13.449282
    },
    {
        'name': 'Riesi',
        'ref': '1363-002',
        'latitude': 47.317,
        'longitude': 8.201
    },
    # ... more components
]
```

**Reference Format**:
- Pattern: `{id_no}-{component_number}`
- Example: `"1363-061"` = Site 1363, Component 61
- Some refs use letters: `"570ter"`

---

## Data Quality Notes

### Missing Data Summary
| Field | Missing Count | Notes |
|-------|---------------|-------|
| `coordinates` | 1 site | Handle with fallback to country centroid |
| `area_hectares` | 23 sites | Display as "Not reported" |
| `main_image_url` | 21 sites | Use placeholder image |
| `cultural_criteria` | ~276 sites | Null for Natural/Mixed sites |
| `natural_criteria` | ~1,013 sites | Null for Cultural sites |
| `danger_list` | ~1,195 sites | Null unless endangered |
| `date_end` | ~1,246 sites | Null unless delisted |

### String Encoding
- All text fields use UTF-8
- Multilingual fields (AR, RU, ZH) use Unicode characters
- Some names include special characters: `'`, `-`, `.`, `,`

### Data Consistency
- All sites have complete name fields (6 languages)
- All sites have descriptions (6 languages short + 2 English long)
- Geographic data highly complete (only 1 missing coordinate)
- Image data mostly complete (21 missing main images)

---

## Normalization Recommendations

### Booleans
```python
# Convert string booleans to actual booleans
site['is_transboundary'] = site['transboundary'] == 'True'
site['is_endangered'] = site['danger'] == 'True'
```

### Arrays
```python
# Convert comma-separated strings to arrays
site['iso_codes_list'] = [c.strip() for c in site['iso_codes'].split(',')]
site['image_gallery'] = [u.strip() for u in site['images_urls'].split(',')] if site['images_urls'] else []
```

### Dates
```python
# Convert date strings to integers
site['year_inscribed'] = int(site['date_inscribed'])
site['secondary_years'] = [int(d.strip()) for d in site['secondary_dates'].split(',')] if site['secondary_dates'] else []
```

### Criteria
```python
# Parse criteria to structured format
cultural = site.get('cultural_criteria')
natural = site.get('natural_criteria')

site['criteria'] = {
    'cultural': [int(c.strip('c')) for c in cultural.split(',')] if cultural else [],
    'natural': [int(n.strip('n')) for n in natural.split(',')] if natural else [],
}
```

---

## Query Patterns

### Get All Sites by Country
```python
def get_sites_by_country(data, iso3_code):
    """Get all sites for a country using ISO3 code."""
    iso2_code = ISO3_TO_ISO2[iso3_code]

    sites = []
    for site in data:
        iso_codes = site['iso_codes'].split(',')
        iso_codes = [c.strip() for c in iso_codes]

        if iso2_code in iso_codes:
            sites.append(site)

    return sites
```

### Get Endangered Sites
```python
endangered = [s for s in data if s['danger'] == 'True']
```

### Get Sites by Criteria
```python
def get_sites_with_criteria(data, criterion):
    """Get sites matching specific criterion (e.g., 'c1', 'n7')."""
    sites = []
    for site in data:
        if criterion.startswith('c'):
            criteria = site.get('cultural_criteria', '')
        else:
            criteria = site.get('natural_criteria', '')

        if criteria and criterion in criteria:
            sites.append(site)

    return sites
```

### Get Transboundary Sites
```python
transboundary = [s for s in data if s['transboundary'] == 'True']
```

---

## Output Format Recommendations

Based on user preference for dictionaries over arrays:

### Countries (Nested Dict)
```json
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

### Criteria (Nested Dict)
```json
"criteria": {
  "cultural": {
    "c1": {"met": true, "display": "(i)"},
    "c2": {"met": true, "display": "(ii)"},
    "c3": {"met": true, "display": "(iii)"}
  },
  "natural": {
    "n7": {"met": false, "display": "(vii)"},
    "n8": {"met": false, "display": "(viii)"}
  }
}
```

### Images (Dict)
```json
"images": {
  "main": {
    "url": "...",
    "dimensions": {"width": 1840, "height": 1232}
  },
  "gallery": {
    "image_001": {"url": "...", "index": 1},
    "image_002": {"url": "...", "index": 2}
  }
}
```
