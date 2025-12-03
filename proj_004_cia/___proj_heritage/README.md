# UNESCO World Heritage Data Processing System

**Version:** 1.0.0
**Last Updated:** December 2025
**Total Sites:** 1,248 UNESCO World Heritage Sites across 170 countries

---

## 🌍 Overview

Complete data processing system for UNESCO World Heritage sites. Processes raw JSON data from 1,248 sites across 170 countries, transforming it into structured, normalized datasets with enhanced metadata for maximum public value.

### Key Features

- **Complete Coverage**: All 1,248 UNESCO World Heritage Sites
- **170 Countries**: Full ISO2→ISO3 mapping
- **6 Languages**: Names and descriptions in EN, FR, ES, RU, AR, ZH
- **Multiple Formats**: JSON, GeoJSON, CSV, Lightweight
- **Enhanced Metadata**: UNESCO URLs, geographic context, historical context
- **Public-Ready**: Optimized for web applications, mapping tools, data analysis

---

## 📊 Quick Stats

| Metric | Count |
|--------|-------|
| **Total Sites** | 1,248 |
| **Countries** | 170 |
| **Cultural Sites** | 972 (77.9%) |
| **Natural Sites** | 235 (18.8%) |
| **Mixed Sites** | 41 (3.3%) |
| **Transboundary** | 51 |
| **Endangered** | 53 |
| **Regions** | 5 UNESCO regions |

---

## 🚀 Quick Start

```python
from proj_004_cia.___proj_heritage.e_01_extract import run_full_pipeline

# Process all data and export products
data = run_full_pipeline(export_products=True)

# Access results
sites = data['normalized_sites']
print(f"Processed {len(sites)} sites")

# Get a specific site
butrint = data['indexes']['by_key']['butrint']
print(f"{butrint['names']['en']}: {butrint['links']['unesco_official']}")
```

---

## 📁 Output Products

All processed data is exported to `y_to_product/` in multiple formats:

### 1. Individual Sites
**Location**: `y_to_product/sites_by_key/`
**Count**: 1,247 files
**Format**: JSON
**Example**: `butrint.json`

### 2. By Country
**Location**: `y_to_product/sites_by_country/`
**Count**: 170 files
**Format**: JSON
**Example**: `FRA.json` (all French sites)

### 3. By Region
**Location**: `y_to_product/sites_by_region/`
**Count**: 5 files
**Format**: JSON
**Files**: `EUR.json`, `ASP.json`, `LAC.json`, `AFR.json`, `ARB.json`

### 4. By Category
**Location**: `y_to_product/sites_by_category/`
**Count**: 3 files
**Format**: JSON
**Files**: `cultural.json`, `natural.json`, `mixed.json`

### 5. Special Collections
**Location**: `y_to_product/special_collections/`
**Count**: 5 files
**Collections**:
- `transboundary.json` - 51 sites spanning multiple countries
- `endangered.json` - 53 sites on UNESCO Danger List
- `large_sites.json` - Sites over 1,000,000 hectares
- `recent_inscriptions.json` - Sites inscribed in last 5 years
- `multi_component.json` - Sites with 10+ components

### 6. GeoJSON (Mapping)
**Location**: `y_to_product/complete/`
**Files**:
- `all_heritage_sites.geojson` - All sites with coordinates
- `y_to_product/geojson_by_country/{ISO3}.geojson` - Per-country GeoJSON

**Use With**: Mapbox, Leaflet, Google Maps, QGIS

### 7. CSV (Analysis)
**Location**: `y_to_product/complete/`
**Files**:
- `all_heritage_sites.csv` - Full dataset (22 columns)
- `heritage_sites_summary.csv` - Key fields only (6 columns)

**Use With**: Excel, Google Sheets, pandas, R

### 8. Lightweight (APIs)
**Location**: `y_to_product/complete/`
**Files**:
- `heritage_sites_lightweight.json` - Essential fields only
- `api_index.json` - Site keys and names for discovery

**Use With**: Web APIs, mobile apps, quick lookups

---

## 🔍 Data Structure

Each normalized site contains:

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

  "geography": {
    "coordinates": {"latitude": 39.745732, "longitude": 20.02095},
    "countries": {
      "ALB": {"name": "Albania", "iso2": "AL", "iso3": "ALB"}
    },
    "region": {"name": "Europe and North America", "code": "EUR"},
    "is_transboundary": false
  },

  "geographic_context": {
    "continent": "Europe",
    "geographic_type": "Urban",
    "has_coordinates": true
  },

  "classification": {
    "category": {"name": "Cultural", "id": 1},
    "criteria": {
      "cultural": [3],
      "natural": [],
      "display": "(iii)",
      "count": 1
    },
    "area": {"hectares": null, "available": false}
  },

  "temporal": {
    "inscription": {
      "primary_date": 1992,
      "all_dates": [1992, 1999],
      "extensions": [1999]
    },
    "danger_status": {
      "is_endangered": false
    }
  },

  "historical_context": {
    "decade": "1990s",
    "era": "Growth Period (1990-1999)",
    "age_years": 33
  },

  "links": {
    "unesco_official": "https://whc.unesco.org/en/list/570",
    "unesco_documents": "https://whc.unesco.org/en/list/570/documents",
    "unesco_gallery": "https://whc.unesco.org/en/list/570/gallery"
  },

  "visual": {
    "main_image": {
      "url": "https://data.unesco.org/...",
      "dimensions": {"width": 1840, "height": 1232}
    },
    "gallery": {
      "urls": ["https://whc.unesco.org/..."],
      "count": 50
    }
  },

  "metadata": {
    "data_source": "UNESCO World Heritage Centre",
    "license": "UNESCO Copyright",
    "attribution": "Data provided by UNESCO World Heritage Centre"
  }
}
```

---

## 🗺️ Usage Examples

### Web Mapping (GeoJSON)

```javascript
// Load GeoJSON in Leaflet/Mapbox
fetch('y_to_product/complete/all_heritage_sites.geojson')
  .then(res => res.json())
  .then(data => {
    L.geoJSON(data, {
      onEachFeature: (feature, layer) => {
        layer.bindPopup(`<b>${feature.properties.name}</b><br>
          ${feature.properties.category}<br>
          <a href="${feature.properties.unesco_url}">UNESCO Page</a>`);
      }
    }).addTo(map);
  });
```

### Data Analysis (CSV)

```python
import pandas as pd

# Load CSV
df = pd.read_csv('y_to_product/complete/all_heritage_sites.csv')

# Analysis
print(df.groupby('continent')['name_en'].count())
print(df[df['is_endangered'] == True][['name_en', 'countries']])
```

### Web API (Lightweight JSON)

```javascript
// Fetch lightweight data for quick lists
fetch('y_to_product/complete/heritage_sites_lightweight.json')
  .then(res => res.json())
  .then(data => {
    data.sites.forEach(site => {
      console.log(`${site.name} (${site.countries.join(', ')})`);
    });
  });
```

---

## 📖 Documentation

- **[ARCHITECTURE.md](_docs/ARCHITECTURE.md)** - Complete system design
- **[DATA_DICTIONARY.md](_docs/DATA_DICTIONARY.md)** - All 37 field definitions
- **[ISO2_TO_ISO3_MAPPING.md](_docs/ISO2_TO_ISO3_MAPPING.md)** - Country code mappings
- **[PROCESSING_NOTES.md](_docs/PROCESSING_NOTES.md)** - Edge cases and best practices

---

## 🔧 System Architecture

```
___proj_heritage/
├── __config/          Configuration & ISO mappings
├── __utils/           6 utility modules
├── a_01_load/         Data loader (1,248 sites)
├── b_01_transform/    8 attribute parsers
│   ├── identity/
│   ├── geographic/
│   ├── descriptive/
│   ├── classification/
│   ├── temporal/
│   ├── visual/
│   ├── components/
│   └── enhancements/  🆕 URLs, metadata, context
├── c_01_normalize/    Normalization & validation
├── d_01_aggregate/    5 aggregation modules
├── e_01_extract/      Main pipeline
├── x_return/          Export in multiple formats
│   ├── JSON
│   ├── GeoJSON      🆕
│   ├── CSV          🆕
│   └── Lightweight  🆕
└── y_to_product/      Output products
```

---

## 📄 License & Attribution

**Data Source**: UNESCO World Heritage Centre
**Data Provider**: UNESCO
**License**: UNESCO Copyright
**Attribution**: Data provided by UNESCO World Heritage Centre (whc.unesco.org)

**System Code**: MIT License
**Author**: Bayoa HT
**Repository**: solve_cia/proj_004_cia

---

## 🌟 Public Value Enhancements

This system includes enhancements specifically for public consumption:

1. ✅ **UNESCO Official URLs** - Direct links to official pages
2. ✅ **Geographic Context** - Continent, geographic type
3. ✅ **Historical Context** - Decade, era, age
4. ✅ **GeoJSON Export** - For mapping applications
5. ✅ **CSV Export** - For spreadsheet analysis
6. ✅ **Lightweight JSON** - For web APIs
7. ✅ **Search-Ready Text** - Full-text search fields
8. ✅ **Enhanced Metadata** - Source, license, attribution

---

## 📞 Contact & Support

For issues, questions, or contributions:
- **GitHub**: BayoatHT/solve_cia
- **Project**: proj_004_cia/___proj_heritage
