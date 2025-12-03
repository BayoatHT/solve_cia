"""
Export heritage sites as GeoJSON for mapping applications.
"""

import json
from pathlib import Path
from typing import Dict, List
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.___proj_heritage.__config.config import Config


def export_geojson(normalized_sites: List[Dict], output_path: Path = None) -> None:
    """
    Export sites as GeoJSON FeatureCollection.

    Args:
        normalized_sites: List of normalized site dictionaries
        output_path: Optional custom output path

    Creates:
        y_to_product/complete/all_heritage_sites.geojson
    """
    app_logger.info("Exporting GeoJSON...")

    if output_path is None:
        output_dir = Config.get_product_path('complete')
        output_path = output_dir / 'all_heritage_sites.geojson'

    # Build GeoJSON FeatureCollection
    features = []

    for site in normalized_sites:
        # Skip sites without coordinates
        coords = site['geography']['coordinates']
        if not coords['available']:
            continue

        # Build feature
        feature = {
            'type': 'Feature',
            'id': site['site_key'],
            'geometry': {
                'type': 'Point',
                'coordinates': [
                    coords['longitude'],  # GeoJSON uses lon, lat order
                    coords['latitude']
                ]
            },
            'properties': {
                'site_key': site['site_key'],
                'name': site['names']['en'],
                'unesco_id': site['unesco_id'],
                'category': site['classification']['category']['name'],
                'criteria_count': site['classification']['criteria']['count'],
                'countries': list(site['geography']['countries'].keys()),
                'region': site['geography']['region']['name'],
                'inscription_year': site['temporal']['inscription']['primary_date'],
                'is_transboundary': site['geography']['is_transboundary'],
                'is_endangered': site['temporal']['danger_status']['is_endangered'],
                'has_image': site['visual']['main_image']['available'],
                'unesco_url': site['links']['unesco_official'],
                'continent': site['geographic_context']['continent'],
                'geographic_type': site['geographic_context']['geographic_type'],
            }
        }

        features.append(feature)

    geojson = {
        'type': 'FeatureCollection',
        'metadata': {
            'generated': site['metadata']['last_updated'] if features else None,
            'source': 'UNESCO World Heritage Centre',
            'total_features': len(features),
            'crs': {
                'type': 'name',
                'properties': {
                    'name': 'EPSG:4326'  # WGS84
                }
            }
        },
        'features': features
    }

    # Export
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, indent=2, ensure_ascii=False)

    app_logger.success(f"✓ Exported {len(features)} sites as GeoJSON")


def export_geojson_by_country(aggregations: Dict, indexes: Dict) -> None:
    """
    Export separate GeoJSON files for each country.

    Args:
        aggregations: Aggregation data
        indexes: Site indexes

    Creates:
        y_to_product/geojson_by_country/{iso3}.geojson
    """
    app_logger.info("Exporting GeoJSON by country...")

    output_dir = Config.PRODUCT_DIR / 'geojson_by_country'
    output_dir.mkdir(parents=True, exist_ok=True)

    by_country = aggregations['by_country']

    for iso3, country_data in by_country.items():
        features = []

        for site_key in country_data['sites']:
            site = indexes['by_key'].get(site_key)
            if not site:
                continue

            coords = site['geography']['coordinates']
            if not coords['available']:
                continue

            feature = {
                'type': 'Feature',
                'id': site_key,
                'geometry': {
                    'type': 'Point',
                    'coordinates': [coords['longitude'], coords['latitude']]
                },
                'properties': {
                    'site_key': site_key,
                    'name': site['names']['en'],
                    'unesco_id': site['unesco_id'],
                    'category': site['classification']['category']['name'],
                    'inscription_year': site['temporal']['inscription']['primary_date'],
                    'unesco_url': site['links']['unesco_official'],
                }
            }

            features.append(feature)

        if features:
            geojson = {
                'type': 'FeatureCollection',
                'metadata': {
                    'country_code': iso3,
                    'country_name': country_data['country_name'],
                    'total_features': len(features),
                },
                'features': features
            }

            file_path = output_dir / f"{iso3}.geojson"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(geojson, f, indent=2, ensure_ascii=False)

    app_logger.success(f"✓ Exported GeoJSON for {len(by_country)} countries")
