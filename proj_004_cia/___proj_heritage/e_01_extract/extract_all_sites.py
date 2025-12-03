"""
Main extraction pipeline orchestrator.

Runs the complete heritage data processing workflow.
"""

from typing import Dict
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.___proj_heritage.a_01_load import load_heritage_data
from proj_004_cia.___proj_heritage.c_01_normalize import (
    normalize_all_sites,
    validate_all_sites,
    build_site_index,
    get_normalization_stats
)
from proj_004_cia.___proj_heritage.d_01_aggregate import (
    aggregate_by_country,
    aggregate_by_region,
    aggregate_by_category,
    aggregate_by_criteria,
    create_special_collections
)


def extract_all_sites() -> Dict:
    """
    Run complete extraction pipeline for all heritage sites.

    Returns:
        Dictionary with all processed data:
        - normalized_sites: List of normalized sites
        - indexes: Lookup indexes
        - aggregations: All aggregated data
        - stats: Statistics

    Example:
        >>> data = extract_all_sites()
        >>> data['stats']['total_sites']
        1248
    """
    app_logger.info("=" * 60)
    app_logger.info("WORLD HERITAGE DATA EXTRACTION PIPELINE")
    app_logger.info("=" * 60)

    # Step 1: Load raw data
    app_logger.info("\n[Step 1/5] Loading raw data...")
    raw_sites = load_heritage_data()

    # Step 2: Normalize all sites
    app_logger.info("\n[Step 2/5] Normalizing sites...")
    normalized_sites = normalize_all_sites(raw_sites)

    # Step 3: Validate
    app_logger.info("\n[Step 3/5] Validating normalized data...")
    validation_results = validate_all_sites(normalized_sites)

    # Build indexes
    app_logger.info("\n[Step 4/5] Building indexes...")
    indexes = build_site_index(normalized_sites)

    # Step 5: Aggregate
    app_logger.info("\n[Step 5/5] Aggregating data...")

    aggregations = {
        'by_country': aggregate_by_country(normalized_sites),
        'by_region': aggregate_by_region(normalized_sites),
        'by_category': aggregate_by_category(normalized_sites),
        'by_criteria': aggregate_by_criteria(normalized_sites),
        'special_collections': create_special_collections(normalized_sites),
    }

    # Get statistics
    stats = get_normalization_stats(normalized_sites)

    # Compile results
    results = {
        'normalized_sites': normalized_sites,
        'indexes': indexes,
        'aggregations': aggregations,
        'validation': validation_results,
        'stats': stats,
    }

    app_logger.info("\n" + "=" * 60)
    app_logger.success("✓ EXTRACTION PIPELINE COMPLETE")
    app_logger.info("=" * 60)
    app_logger.info(f"Total sites processed: {stats['total_sites']}")
    app_logger.info(f"Valid sites: {validation_results['valid_count']}")
    app_logger.info(f"Countries: {len(aggregations['by_country'])}")
    app_logger.info(f"Regions: {len(aggregations['by_region'])}")
    app_logger.info("=" * 60)

    return results


def run_full_pipeline(export_products: bool = False) -> Dict:
    """
    Run the full pipeline including optional product export.

    Args:
        export_products: If True, export all data products to files

    Returns:
        Dictionary with all processed data

    Example:
        >>> data = run_full_pipeline(export_products=True)
        >>> # Creates all JSON product files
    """
    # Extract all data
    data = extract_all_sites()

    # Export products if requested
    if export_products:
        app_logger.info("\nExporting data products...")
        from proj_004_cia.___proj_heritage.x_return import export_all_products
        export_all_products(data)

    return data
