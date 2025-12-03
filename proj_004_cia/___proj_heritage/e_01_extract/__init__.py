"""
Main extraction pipeline for World Heritage data processing.

Orchestrates the complete data processing workflow:
1. Load raw data
2. Normalize all sites
3. Aggregate by various attributes
4. Export to products
"""

from .extract_all_sites import extract_all_sites, run_full_pipeline

__all__ = [
    'extract_all_sites',
    'run_full_pipeline',
]
