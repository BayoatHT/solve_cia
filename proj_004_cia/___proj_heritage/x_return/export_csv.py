"""
Export heritage sites as CSV for spreadsheet analysis.
"""

import csv
from pathlib import Path
from typing import Dict, List
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.___proj_heritage.__config.config import Config


def export_csv(normalized_sites: List[Dict], output_path: Path = None) -> None:
    """
    Export sites as CSV file.

    Args:
        normalized_sites: List of normalized site dictionaries
        output_path: Optional custom output path

    Creates:
        y_to_product/complete/all_heritage_sites.csv
    """
    app_logger.info("Exporting CSV...")

    if output_path is None:
        output_dir = Config.get_product_path('complete')
        output_path = output_dir / 'all_heritage_sites.csv'

    # Define CSV columns
    columns = [
        'site_key',
        'name_en',
        'unesco_id',
        'category',
        'criteria_display',
        'criteria_count',
        'countries',
        'region',
        'continent',
        'latitude',
        'longitude',
        'inscription_year',
        'inscription_decade',
        'age_years',
        'is_transboundary',
        'is_endangered',
        'area_hectares',
        'has_image',
        'components_count',
        'geographic_type',
        'unesco_url',
        'description_en',
    ]

    # Prepare rows
    rows = []
    for site in normalized_sites:
        coords = site['geography']['coordinates']
        area = site['classification']['area']

        row = {
            'site_key': site['site_key'],
            'name_en': site['names'].get('en', ''),
            'unesco_id': site['unesco_id'],
            'category': site['classification']['category']['name'],
            'criteria_display': site['classification']['criteria']['display'],
            'criteria_count': site['classification']['criteria']['count'],
            'countries': ', '.join(site['geography']['countries'].keys()),
            'region': site['geography']['region']['name'],
            'continent': site['geographic_context']['continent'],
            'latitude': coords['latitude'] if coords['available'] else None,
            'longitude': coords['longitude'] if coords['available'] else None,
            'inscription_year': site['temporal']['inscription']['primary_date'],
            'inscription_decade': site['historical_context']['decade'],
            'age_years': site['historical_context']['age_years'],
            'is_transboundary': site['geography']['is_transboundary'],
            'is_endangered': site['temporal']['danger_status']['is_endangered'],
            'area_hectares': area['hectares'] if area['available'] else None,
            'has_image': site['visual']['main_image']['available'],
            'components_count': site['components']['count'],
            'geographic_type': site['geographic_context']['geographic_type'],
            'unesco_url': site['links']['unesco_official'],
            'description_en': site['descriptions']['short'].get('en', '')[:500],  # Truncate
        }
        rows.append(row)

    # Export CSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    app_logger.success(f"✓ Exported {len(rows)} sites as CSV")


def export_csv_summary(normalized_sites: List[Dict], output_path: Path = None) -> None:
    """
    Export minimal CSV with key fields only.

    Args:
        normalized_sites: List of normalized sites
        output_path: Optional output path

    Creates:
        y_to_product/complete/heritage_sites_summary.csv
    """
    app_logger.info("Exporting summary CSV...")

    if output_path is None:
        output_dir = Config.get_product_path('complete')
        output_path = output_dir / 'heritage_sites_summary.csv'

    columns = [
        'site_key',
        'name',
        'country',
        'category',
        'inscription_year',
        'unesco_url',
    ]

    rows = []
    for site in normalized_sites:
        # Get primary country (first in list)
        countries = list(site['geography']['countries'].keys())
        primary_country = countries[0] if countries else 'Unknown'

        row = {
            'site_key': site['site_key'],
            'name': site['names'].get('en', ''),
            'country': primary_country,
            'category': site['classification']['category']['name'],
            'inscription_year': site['temporal']['inscription']['primary_date'],
            'unesco_url': site['links']['unesco_official'],
        }
        rows.append(row)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    app_logger.success(f"✓ Exported {len(rows)} sites as summary CSV")
