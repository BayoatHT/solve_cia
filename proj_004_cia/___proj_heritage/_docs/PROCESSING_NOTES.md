# World Heritage Data - Processing Notes

Edge cases, special handling, and implementation notes for the heritage data processing system.

---

## Critical Edge Cases

### 1. Missing Coordinates (1 site)

**Issue**: One site has `null` coordinates
**Impact**: Cannot display on map
**Solution**:
```python
def get_coordinates(site):
    """Get site coordinates with fallback."""
    coords = site.get('coordinates')
    if coords and coords.get('lat') and coords.get('lon'):
        return {
            'latitude': coords['lat'],
            'longitude': coords['lon'],
            'source': 'site'
        }

    # Fallback: use country centroid
    iso2_codes = site['iso_codes'].split(',')
    first_country = iso2_codes[0].strip()
    iso3 = ISO2_TO_ISO3[first_country]

    return {
        'latitude': COUNTRY_CENTROIDS[iso3]['lat'],
        'longitude': COUNTRY_CENTROIDS[iso3]['lon'],
        'source': 'country_centroid',
        'note': 'Site coordinates not available'
    }
```

---

### 2. Missing Area (23 sites)

**Issue**: 23 sites have `null` area_hectares
**Impact**: Cannot compare sizes or calculate density
**Solution**:
```python
def format_area(area_hectares):
    """Format area with null handling."""
    if area_hectares is None:
        return {
            'value': None,
            'formatted': 'Not reported',
            'hectares': None,
            'sq_km': None,
            'sq_mi': None
        }

    return {
        'value': area_hectares,
        'formatted': f"{area_hectares:,.0f} hectares",
        'hectares': area_hectares,
        'sq_km': area_hectares / 100,
        'sq_mi': area_hectares / 247.105
    }
```

---

### 3. Missing Main Image (21 sites)

**Issue**: 21 sites have `null` main_image_url
**Impact**: Cannot display preview image
**Solution**:
```python
def get_main_image(site):
    """Get main image with fallback."""
    main_img = site.get('main_image_url')

    if main_img:
        return {
            'url': main_img['url'],
            'filename': main_img['filename'],
            'dimensions': {
                'width': main_img['width'],
                'height': main_img['height']
            },
            'format': main_img.get('format', 'JPEG'),
            'color_palette': main_img.get('color_summary', []),
            'source': 'unesco'
        }

    # Fallback: check if images_urls has any images
    if site.get('images_urls'):
        gallery = site['images_urls'].split(',')
        if gallery:
            return {
                'url': gallery[0].strip(),
                'filename': None,
                'dimensions': None,
                'format': 'JPEG',
                'color_palette': [],
                'source': 'gallery_first'
            }

    # Ultimate fallback: placeholder
    category = site['category'].lower()
    return {
        'url': f'/placeholders/{category}_placeholder.jpg',
        'filename': None,
        'dimensions': None,
        'format': 'JPEG',
        'color_palette': [],
        'source': 'placeholder'
    }
```

---

### 4. Transboundary Sites (51 sites)

**Challenge**: Sites span multiple countries

**Strategy 1: Duplicate Representation**
```python
# Store site under each country
def distribute_to_countries(site):
    """Create country-specific entries for transboundary sites."""
    iso2_codes = [c.strip() for c in site['iso_codes'].split(',')]
    iso3_codes = [ISO2_TO_ISO3[code] for code in iso2_codes]

    entries = {}
    for iso3 in iso3_codes:
        entry = site.copy()
        entry['primary_country'] = iso3
        entry['is_transboundary'] = True
        entry['all_countries'] = iso3_codes
        entries[iso3] = entry

    return entries

# Result: Each country sees the site in their list
```

**Strategy 2: Shared Reference**
```python
# Store once, reference from multiple countries
{
  "sites": {
    "prehistoric_pile_dwellings": { /* full data */ }
  },
  "countries": {
    "ITA": {
      "sites": ["prehistoric_pile_dwellings", "..."]
    },
    "FRA": {
      "sites": ["prehistoric_pile_dwellings", "..."]
    }
  }
}
```

**Recommendation**: Use Strategy 1 for country views, Strategy 2 for global index

---

### 5. Components Parsing

**Challenge**: Components stored as pseudo-JSON string

**Input**:
```
"{name: See , ref: 1363-061, latitude: 47.803881, longitude: 13.449282}, {name: Riesi, ref: 1363-002, latitude: 47.317, longitude: 8.201}"
```

**Robust Parser**:
```python
import re

def parse_components(components_str):
    """Parse components string robustly."""
    if not components_str:
        return []

    # Handle edge cases
    components_str = components_str.strip()
    if not components_str.startswith('{'):
        return []

    # Split by component boundaries
    # Pattern: }, { or }   {  (with variable whitespace)
    component_strings = re.split(r'\}\s*,?\s*\{', components_str)

    components = []
    for comp_str in component_strings:
        # Clean boundaries
        comp_str = comp_str.strip('{}').strip()

        # Parse key-value pairs
        component = {}

        # Pattern: key: value
        for match in re.finditer(r'(\w+):\s*([^,}]+?)(?=,\s*\w+:|$)', comp_str):
            key = match.group(1).strip()
            value = match.group(2).strip()

            # Type conversion
            if key in ['latitude', 'longitude']:
                try:
                    component[key] = float(value)
                except (ValueError, TypeError):
                    component[key] = None
            else:
                component[key] = value

        if component and 'name' in component:
            components.append(component)

    return components

# Test edge cases
test_cases = [
    "{name: Single}",  # Single component
    "{name: A}, {name: B}",  # Multiple
    "{name: Trailing spaces , ref: 123  }",  # Whitespace
    "",  # Empty
    "{malformed",  # Invalid
]
```

**Edge Cases**:
- Extra whitespace in values
- Missing fields (some components lack ref or coordinates)
- Special characters in names (commas, apostrophes)
- Trailing/leading braces

---

### 6. Image URLs Parsing

**Challenge**: Very long comma-separated string (100+ URLs)

**Efficient Parser**:
```python
def parse_image_gallery(images_urls_str, max_images=None):
    """Parse image gallery with optional limit."""
    if not images_urls_str:
        return []

    # Split and clean
    urls = [url.strip() for url in images_urls_str.split(',')]

    # Filter valid URLs
    urls = [url for url in urls if url.startswith('http')]

    # Apply limit if specified
    if max_images:
        urls = urls[:max_images]

    return urls

# Usage
gallery = parse_image_gallery(site['images_urls'], max_images=20)
# First 20 images for initial load, lazy-load rest
```

---

### 7. Criteria Parsing

**Challenge**: Multiple formats (comma-separated codes, Roman numerals)

**Unified Parser**:
```python
def parse_criteria(site):
    """Parse all criteria formats into unified structure."""
    cultural = site.get('cultural_criteria', '')
    natural = site.get('natural_criteria', '')

    criteria = {
        'cultural': [],
        'natural': [],
        'all': [],
        'display': site['criteria_txt'],
        'count': 0
    }

    # Parse cultural criteria
    if cultural:
        codes = [c.strip() for c in cultural.split(',')]
        criteria['cultural'] = [int(c.replace('c', '')) for c in codes]

    # Parse natural criteria
    if natural:
        codes = [c.strip() for c in natural.split(',')]
        criteria['natural'] = [int(c.replace('n', '')) for c in codes]

    # Combine
    criteria['all'] = criteria['cultural'] + criteria['natural']
    criteria['count'] = len(criteria['all'])

    # Validate against display text
    expected_count = site['criteria_txt'].count('(')
    if criteria['count'] != expected_count:
        # Log warning: criteria mismatch
        pass

    return criteria

# Example output
{
    'cultural': [1, 2, 3],
    'natural': [],
    'all': [1, 2, 3],
    'display': '(i)(ii)(iii)',
    'count': 3
}
```

---

### 8. Secondary Dates Parsing

**Challenge**: Variable format (single date, multiple dates, empty)

**Parser**:
```python
def parse_inscription_dates(site):
    """Parse inscription and extension dates."""
    primary = int(site['date_inscribed'])
    secondary_str = site.get('secondary_dates', '')

    dates = {
        'primary': primary,
        'all': [primary],
        'extensions': [],
        'timeline': []
    }

    if secondary_str:
        all_dates = [int(d.strip()) for d in secondary_str.split(',')]
        dates['all'] = sorted(all_dates)

        # Identify extensions (dates after primary)
        dates['extensions'] = [d for d in all_dates if d > primary]

        # Build timeline
        dates['timeline'] = [
            {'year': primary, 'event': 'Inscribed'}
        ]
        for ext_date in dates['extensions']:
            dates['timeline'].append({
                'year': ext_date,
                'event': 'Extended'
            })

    return dates

# Example output
{
    'primary': 1992,
    'all': [1992, 1999, 2005],
    'extensions': [1999, 2005],
    'timeline': [
        {'year': 1992, 'event': 'Inscribed'},
        {'year': 1999, 'event': 'Extended'},
        {'year': 2005, 'event': 'Extended'}
    ]
}
```

---

### 9. Site Key Generation (Uniqueness)

**Challenge**: Ensure unique keys from name_en

**Strategy**:
```python
from slugify import slugify

def generate_site_key(site, existing_keys=set()):
    """Generate unique site key from name_en."""
    base_key = slugify(site['name_en'], separator='_', lowercase=True)

    # Check uniqueness
    if base_key not in existing_keys:
        return base_key

    # Collision: append ISO3 of first country
    iso2_codes = site['iso_codes'].split(',')
    first_iso2 = iso2_codes[0].strip()
    iso3 = ISO2_TO_ISO3[first_iso2]
    key_with_country = f"{base_key}_{iso3.lower()}"

    if key_with_country not in existing_keys:
        return key_with_country

    # Still collision: append UNESCO ID
    key_with_id = f"{base_key}_{site['id_no']}"
    return key_with_id

# Batch processing
def generate_all_keys(sites):
    """Generate keys for all sites ensuring uniqueness."""
    existing_keys = set()
    key_map = {}

    for site in sites:
        key = generate_site_key(site, existing_keys)
        existing_keys.add(key)
        key_map[site['uuid']] = key

    return key_map
```

**Test Cases**:
```python
# Same name different countries
site1 = {"name_en": "Historic Centre", "iso_codes": "CZ", "id_no": "616"}
site2 = {"name_en": "Historic Centre", "iso_codes": "IT", "id_no": "726"}

# Result:
# site1: "historic_centre_cze"
# site2: "historic_centre_ita"
```

---

### 10. Empty String vs Null Handling

**Challenge**: Some fields are empty strings `""` instead of `null`

**Fields to Check**:
- `images_urls` - Can be empty string
- `secondary_dates` - Can be empty string
- `danger_list` - Usually null

**Utility Function**:
```python
def normalize_empty(value):
    """Convert empty strings to None."""
    if value == "" or value == "null" or value == "NULL":
        return None
    return value

# Apply to relevant fields
def clean_site_data(site):
    """Normalize empty values."""
    empty_to_null = ['images_urls', 'secondary_dates', 'danger_list']

    for field in empty_to_null:
        if field in site:
            site[field] = normalize_empty(site[field])

    return site
```

---

## Performance Optimizations

### 1. Lazy Loading Components

**Issue**: Parsing 111 components for every site is expensive

**Solution**:
```python
class HeritageSite:
    def __init__(self, raw_data):
        self._raw = raw_data
        self._components = None  # Lazy load

    @property
    def components(self):
        """Parse components only when accessed."""
        if self._components is None:
            self._components = parse_components(
                self._raw.get('components_list', '')
            )
        return self._components
```

### 2. Index Building

**Strategy**: Pre-build indexes for fast lookups

```python
def build_indexes(sites):
    """Build lookup indexes."""
    indexes = {
        'by_key': {},
        'by_uuid': {},
        'by_country': {},
        'by_region': {},
        'by_category': {},
        'by_year': {}
    }

    for site in sites:
        key = site['site_key']
        uuid = site['uuid']

        # Key index
        indexes['by_key'][key] = site

        # UUID index
        indexes['by_uuid'][uuid] = site

        # Country index
        iso3_codes = site['geography']['countries'].keys()
        for iso3 in iso3_codes:
            if iso3 not in indexes['by_country']:
                indexes['by_country'][iso3] = []
            indexes['by_country'][iso3].append(key)

        # Region index
        region = site['geography']['region']['code']
        if region not in indexes['by_region']:
            indexes['by_region'][region] = []
        indexes['by_region'][region].append(key)

        # Category index
        category = site['classification']['category']['name']
        if category not in indexes['by_category']:
            indexes['by_category'][category] = []
        indexes['by_category'][category].append(key)

        # Year index
        year = site['temporal']['inscription']['primary_date']
        if year not in indexes['by_year']:
            indexes['by_year'][year] = []
        indexes['by_year'][year].append(key)

    return indexes
```

### 3. Caching

**Strategy**: Cache expensive operations

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_site_by_key(key):
    """Cached site lookup."""
    return indexes['by_key'].get(key)

@lru_cache(maxsize=200)
def get_sites_by_country(iso3):
    """Cached country sites."""
    site_keys = indexes['by_country'].get(iso3, [])
    return [get_site_by_key(key) for key in site_keys]
```

---

## Data Validation

### Validation Rules

```python
def validate_site(site):
    """Validate site data completeness and correctness."""
    errors = []
    warnings = []

    # Required fields
    required = ['uuid', 'id_no', 'name_en', 'iso_codes', 'category']
    for field in required:
        if field not in site or site[field] is None:
            errors.append(f"Missing required field: {field}")

    # Coordinate validation
    coords = site.get('coordinates')
    if coords:
        lat, lon = coords.get('lat'), coords.get('lon')
        if lat and (lat < -90 or lat > 90):
            errors.append(f"Invalid latitude: {lat}")
        if lon and (lon < -180 or lon > 180):
            errors.append(f"Invalid longitude: {lon}")
    else:
        warnings.append("Missing coordinates")

    # ISO code validation
    iso_codes = site.get('iso_codes', '')
    for code in iso_codes.split(','):
        code = code.strip()
        if code and code not in ISO2_TO_ISO3:
            errors.append(f"Invalid ISO2 code: {code}")

    # Category validation
    category = site.get('category')
    if category not in ['Cultural', 'Natural', 'Mixed']:
        errors.append(f"Invalid category: {category}")

    # Date validation
    try:
        year = int(site['date_inscribed'])
        if year < 1900 or year > 2030:
            warnings.append(f"Unusual inscription year: {year}")
    except (ValueError, KeyError):
        errors.append("Invalid date_inscribed")

    # Area validation
    area = site.get('area_hectares')
    if area is not None:
        if area < 0:
            errors.append(f"Negative area: {area}")
        elif area > 10000000:  # 100,000 sq km
            warnings.append(f"Unusually large area: {area} ha")

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }
```

### Batch Validation

```python
def validate_dataset(sites):
    """Validate entire dataset."""
    results = {
        'total': len(sites),
        'valid': 0,
        'errors': 0,
        'warnings': 0,
        'details': []
    }

    for site in sites:
        validation = validate_site(site)

        if validation['valid']:
            results['valid'] += 1
        else:
            results['errors'] += 1
            results['details'].append({
                'site': site.get('name_en', 'Unknown'),
                'uuid': site.get('uuid'),
                'errors': validation['errors']
            })

        if validation['warnings']:
            results['warnings'] += 1

    return results
```

---

## Testing Strategies

### Unit Tests

```python
# Test: Site key generation
def test_site_key_generation():
    site = {"name_en": "Palace of Versailles"}
    key = generate_site_key(site)
    assert key == "palace_of_versailles"

# Test: ISO2 to ISO3 conversion
def test_iso_conversion():
    assert ISO2_TO_ISO3['FR'] == 'FRA'
    assert ISO2_TO_ISO3['GB'] == 'GBR'

# Test: Coordinate validation
def test_coordinates():
    coords = {"lat": 39.745732, "lon": 20.02095}
    assert -90 <= coords['lat'] <= 90
    assert -180 <= coords['lon'] <= 180

# Test: Components parsing
def test_components_parsing():
    comp_str = "{name: See, ref: 1363-061, latitude: 47.803881, longitude: 13.449282}"
    result = parse_components(comp_str)
    assert len(result) == 1
    assert result[0]['name'] == 'See'
    assert result[0]['latitude'] == 47.803881
```

### Integration Tests

```python
# Test: Full pipeline
def test_full_pipeline():
    # Load raw data
    sites = load_heritage_data()
    assert len(sites) == 1248

    # Transform
    normalized = [normalize_site(s) for s in sites]
    assert all('site_key' in s for s in normalized)

    # Validate
    validation = validate_dataset(normalized)
    assert validation['valid'] >= 1200  # Allow some warnings

# Test: Country aggregation
def test_country_aggregation():
    sites_fr = get_sites_by_country('FRA')
    assert len(sites_fr) >= 50  # France has 50+ sites

# Test: Transboundary handling
def test_transboundary():
    transboundary = [s for s in sites if s['is_transboundary']]
    assert len(transboundary) == 51
```

---

## Special Collections

### 1. World Records

```python
def get_world_records(sites):
    """Extract interesting site statistics."""
    return {
        'largest_area': max(sites, key=lambda s: s.get('area_hectares') or 0),
        'smallest_area': min(s for s in sites if s.get('area_hectares')),
        'oldest_site': min(sites, key=lambda s: int(s['date_inscribed'])),
        'newest_site': max(sites, key=lambda s: int(s['date_inscribed'])),
        'most_components': max(sites, key=lambda s: s['components_count']),
        'most_countries': max([s for s in sites if s['transboundary'] == 'True'],
                             key=lambda s: len(s['iso_codes'].split(','))),
        'most_criteria': max(sites,
                            key=lambda s: s['criteria_txt'].count('(')),
    }
```

### 2. Statistical Summaries

```python
def generate_statistics(sites):
    """Generate dataset statistics."""
    return {
        'total_sites': len(sites),
        'by_category': {
            'Cultural': len([s for s in sites if s['category'] == 'Cultural']),
            'Natural': len([s for s in sites if s['category'] == 'Natural']),
            'Mixed': len([s for s in sites if s['category'] == 'Mixed']),
        },
        'by_region': {
            region: len([s for s in sites if s['region_code'] == code])
            for code, region in REGION_CODES.items()
        },
        'endangered': len([s for s in sites if s['danger'] == 'True']),
        'transboundary': len([s for s in sites if s['transboundary'] == 'True']),
        'with_images': len([s for s in sites if s.get('main_image_url')]),
        'date_range': {
            'earliest': min(int(s['date_inscribed']) for s in sites),
            'latest': max(int(s['date_inscribed']) for s in sites),
        },
        'area_stats': {
            'mean': sum(s.get('area_hectares', 0) for s in sites) / len(sites),
            'max': max(s.get('area_hectares', 0) for s in sites),
            'sites_with_area': len([s for s in sites if s.get('area_hectares')]),
        }
    }
```

---

## Error Handling Best Practices

### 1. Graceful Degradation

```python
def safe_parse(parser_func, data, default=None):
    """Safely parse data with fallback."""
    try:
        return parser_func(data)
    except Exception as e:
        app_logger.warning(f"Parse failed: {e}, using default: {default}")
        return default

# Usage
components = safe_parse(parse_components, site['components_list'], default=[])
```

### 2. Logging Strategy

```python
from proj_004_cia.__logger.logger import app_logger

# Log levels:
app_logger.debug(f"Processing site: {site['name_en']}")  # Verbose
app_logger.info(f"Processed {count} sites")  # Progress
app_logger.warning(f"Missing coordinates for {site['name_en']}")  # Recoverable
app_logger.error(f"Failed to parse site {uuid}")  # Serious
app_logger.success(f"✓ All {count} sites processed successfully")  # Completion
```

### 3. Data Quality Reports

```python
def generate_quality_report(sites):
    """Generate data quality report."""
    report = {
        'total_sites': len(sites),
        'issues': {
            'missing_coordinates': [],
            'missing_area': [],
            'missing_images': [],
            'invalid_codes': [],
        }
    }

    for site in sites:
        if not site.get('coordinates'):
            report['issues']['missing_coordinates'].append(site['name_en'])

        if site.get('area_hectares') is None:
            report['issues']['missing_area'].append(site['name_en'])

        if not site.get('main_image_url'):
            report['issues']['missing_images'].append(site['name_en'])

    return report
```

---

## Implementation Checklist

- [ ] Create folder structure
- [ ] Implement ISO2→ISO3 mapping
- [ ] Implement site key generation
- [ ] Implement all attribute parsers
- [ ] Handle null values for coordinates, area, images
- [ ] Parse transboundary sites correctly
- [ ] Parse components robustly
- [ ] Parse image gallery efficiently
- [ ] Build country aggregation
- [ ] Build region aggregation
- [ ] Generate individual site files
- [ ] Validate all 1,248 sites
- [ ] Generate data quality report
- [ ] Create indexes for fast lookup
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Document API
- [ ] Performance optimization

---

## Next Steps After Review

1. User reviews architecture
2. Implement Phase 1: Foundation
   - Create folder structure
   - Implement config and ISO mapping
   - Implement utilities
3. Implement Phase 2: Parsers
   - One parser at a time
   - Test each parser
4. Implement Phase 3: Normalization
5. Implement Phase 4: Aggregation
6. Implement Phase 5: Export
7. Validate complete dataset
8. Generate final products
