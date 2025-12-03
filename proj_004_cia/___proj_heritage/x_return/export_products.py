"""
Export processed data to JSON product files.
"""

import json
from pathlib import Path
from typing import Dict, List
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.___proj_heritage.__config.config import Config


def export_json(data: Dict, file_path: Path) -> None:
    """
    Export data to JSON file with pretty formatting.

    Args:
        data: Data to export
        file_path: Path to JSON file
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(
            data,
            f,
            indent=Config.JSON_INDENT if Config.PRETTY_JSON else None,
            ensure_ascii=False
        )


def export_sites_by_key(normalized_sites: List[Dict], indexes: Dict) -> None:
    """
    Export individual site files keyed by site_key.

    Args:
        normalized_sites: List of normalized sites
        indexes: Site indexes

    Creates:
        y_to_product/sites_by_key/{site_key}.json (1,248 files)
    """
    app_logger.info("Exporting sites by key...")

    output_dir = Config.get_product_path('sites_by_key')

    for site in normalized_sites:
        site_key = site['site_key']
        file_path = output_dir / f"{site_key}.json"
        export_json(site, file_path)

    app_logger.success(f"✓ Exported {len(normalized_sites)} individual site files")


def export_sites_by_country(aggregations: Dict, indexes: Dict) -> None:
    """
    Export country-grouped data.

    Args:
        aggregations: Aggregation data
        indexes: Site indexes

    Creates:
        y_to_product/sites_by_country/{iso3_code}.json (170 files)
    """
    app_logger.info("Exporting sites by country...")

    output_dir = Config.get_product_path('sites_by_country')
    by_country = aggregations['by_country']

    for iso3, country_data in by_country.items():
        # Get full site data for each site key
        sites = []
        for site_key in country_data['sites']:
            site = indexes['by_key'].get(site_key)
            if site:
                sites.append(site)

        # Build country file
        country_export = {
            'country': {
                'code': country_data['country_code'],
                'name': country_data['country_name'],
            },
            'total_sites': country_data['total_sites'],
            'sites_by_category': country_data['sites_by_category'],
            'transboundary_count': country_data['transboundary_sites'],
            'endangered_count': country_data['endangered_sites'],
            'sites': sites
        }

        file_path = output_dir / f"{iso3}.json"
        export_json(country_export, file_path)

    app_logger.success(f"✓ Exported {len(by_country)} country files")


def export_sites_by_region(aggregations: Dict, indexes: Dict) -> None:
    """
    Export region-grouped data.

    Args:
        aggregations: Aggregation data
        indexes: Site indexes

    Creates:
        y_to_product/sites_by_region/{region_code}.json (5 files)
    """
    app_logger.info("Exporting sites by region...")

    output_dir = Config.get_product_path('sites_by_region')
    by_region = aggregations['by_region']

    for region_code, region_data in by_region.items():
        # Get full site data
        sites = []
        for site_key in region_data['sites']:
            site = indexes['by_key'].get(site_key)
            if site:
                sites.append(site)

        # Build region file
        region_export = {
            'region': {
                'code': region_data['region_code'],
                'name': region_data['region_name'],
            },
            'total_sites': region_data['total_sites'],
            'sites_by_category': region_data['sites_by_category'],
            'countries': region_data['countries'],
            'country_count': region_data['country_count'],
            'sites': sites
        }

        file_path = output_dir / f"{region_code}.json"
        export_json(region_export, file_path)

    app_logger.success(f"✓ Exported {len(by_region)} region files")


def export_sites_by_category(aggregations: Dict, indexes: Dict) -> None:
    """
    Export category-grouped data.

    Args:
        aggregations: Aggregation data
        indexes: Site indexes

    Creates:
        y_to_product/sites_by_category/{category}.json (3 files)
    """
    app_logger.info("Exporting sites by category...")

    output_dir = Config.get_product_path('sites_by_category')
    by_category = aggregations['by_category']

    for category_name, category_data in by_category.items():
        # Get full site data
        sites = []
        for site_key in category_data['sites']:
            site = indexes['by_key'].get(site_key)
            if site:
                sites.append(site)

        # Build category file
        category_export = {
            'category': {
                'name': category_name,
                'id': category_data['category_id'],
            },
            'total_sites': category_data['total_sites'],
            'sites': sites
        }

        file_path = output_dir / f"{category_name.lower()}.json"
        export_json(category_export, file_path)

    app_logger.success(f"✓ Exported {len(by_category)} category files")


def export_special_collections(aggregations: Dict, indexes: Dict) -> None:
    """
    Export special collections.

    Args:
        aggregations: Aggregation data
        indexes: Site indexes

    Creates:
        y_to_product/special_collections/{collection}.json
    """
    app_logger.info("Exporting special collections...")

    output_dir = Config.get_product_path('special_collections')
    collections = aggregations['special_collections']

    for collection_key, collection_data in collections.items():
        # Get full site data
        sites = []
        for site_key in collection_data['sites']:
            site = indexes['by_key'].get(site_key)
            if site:
                sites.append(site)

        # Build collection file
        collection_export = {
            'collection': {
                'key': collection_key,
                'name': collection_data['name'],
                'description': collection_data['description'],
            },
            'total_sites': collection_data['count'],
            'sites': sites
        }

        file_path = output_dir / f"{collection_key}.json"
        export_json(collection_export, file_path)

    app_logger.success(f"✓ Exported {len(collections)} special collections")


def export_complete_dataset(normalized_sites: List[Dict], aggregations: Dict, stats: Dict) -> None:
    """
    Export complete dataset with metadata.

    Args:
        normalized_sites: All normalized sites
        aggregations: All aggregations
        stats: Dataset statistics

    Creates:
        y_to_product/complete/all_heritage_sites.json
    """
    app_logger.info("Exporting complete dataset...")

    output_dir = Config.get_product_path('complete')

    complete_export = {
        'metadata': {
            'total_sites': len(normalized_sites),
            'categories': dict(stats['by_category']),
            'regions': dict(stats['by_region']),
            'countries': len(aggregations['by_country']),
            'transboundary_count': stats['transboundary_count'],
            'endangered_count': stats['endangered_count'],
        },
        'sites': normalized_sites
    }

    file_path = output_dir / 'all_heritage_sites.json'
    export_json(complete_export, file_path)

    app_logger.success("✓ Exported complete dataset")


def export_all_products(data: Dict) -> None:
    """
    Export all data products.

    Args:
        data: Output from extract_all_sites()

    Creates all product files in y_to_product/
    """
    app_logger.info("\n" + "=" * 60)
    app_logger.info("EXPORTING DATA PRODUCTS")
    app_logger.info("=" * 60)

    # Ensure product directories exist
    Config.ensure_product_dirs()

    normalized_sites = data['normalized_sites']
    indexes = data['indexes']
    aggregations = data['aggregations']
    stats = data['stats']

    # Export all product types
    export_sites_by_key(normalized_sites, indexes)
    export_sites_by_country(aggregations, indexes)
    export_sites_by_region(aggregations, indexes)
    export_sites_by_category(aggregations, indexes)
    export_special_collections(aggregations, indexes)
    export_complete_dataset(normalized_sites, aggregations, stats)

    app_logger.info("=" * 60)
    app_logger.success("✓ ALL PRODUCTS EXPORTED")
    app_logger.info("=" * 60)
