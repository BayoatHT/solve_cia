"""
Export lightweight/summary versions of site data for APIs.
"""

import json
from pathlib import Path
from typing import Dict, List
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.___proj_heritage.__config.config import Config


def create_lightweight_site(site: Dict) -> Dict:
    """
    Create lightweight version of site data (essential fields only).

    Args:
        site: Full normalized site dictionary

    Returns:
        Lightweight site dictionary
    """
    coords = site['geography']['coordinates']

    return {
        'site_key': site['site_key'],
        'name': site['names']['en'],
        'unesco_id': site['unesco_id'],
        'category': site['classification']['category']['name'],
        'countries': list(site['geography']['countries'].keys()),
        'region': site['geography']['region']['code'],
        'coordinates': {
            'lat': coords['latitude'],
            'lon': coords['longitude']
        } if coords['available'] else None,
        'inscription_year': site['temporal']['inscription']['primary_date'],
        'unesco_url': site['links']['unesco_official'],
        'image_url': site['visual']['main_image']['url'] if site['visual']['main_image']['available'] else None,
    }


def export_lightweight(normalized_sites: List[Dict], output_path: Path = None) -> None:
    """
    Export lightweight version of all sites.

    Args:
        normalized_sites: List of normalized sites
        output_path: Optional output path

    Creates:
        y_to_product/complete/heritage_sites_lightweight.json
    """
    app_logger.info("Exporting lightweight JSON...")

    if output_path is None:
        output_dir = Config.get_product_path('complete')
        output_path = output_dir / 'heritage_sites_lightweight.json'

    lightweight_sites = [create_lightweight_site(site) for site in normalized_sites]

    lightweight_export = {
        'metadata': {
            'total_sites': len(lightweight_sites),
            'version': 'lightweight',
            'fields': list(lightweight_sites[0].keys()) if lightweight_sites else [],
        },
        'sites': lightweight_sites
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(lightweight_export, f, indent=2, ensure_ascii=False)

    app_logger.success(f"✓ Exported {len(lightweight_sites)} lightweight sites")


def export_api_index(normalized_sites: List[Dict], output_path: Path = None) -> None:
    """
    Export API index (site keys and names only for discovery).

    Args:
        normalized_sites: List of normalized sites
        output_path: Optional output path

    Creates:
        y_to_product/complete/api_index.json
    """
    app_logger.info("Exporting API index...")

    if output_path is None:
        output_dir = Config.get_product_path('complete')
        output_path = output_dir / 'api_index.json'

    index = []
    for site in normalized_sites:
        index.append({
            'site_key': site['site_key'],
            'name': site['names']['en'],
            'country': list(site['geography']['countries'].keys())[0] if site['geography']['countries'] else None,
            'category': site['classification']['category']['name'],
        })

    api_index = {
        'metadata': {
            'total_sites': len(index),
            'version': 'index',
            'purpose': 'Site discovery and listing',
        },
        'sites': index
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(api_index, f, indent=2, ensure_ascii=False)

    app_logger.success(f"✓ Exported API index with {len(index)} sites")
