"""
u_nation_feature_strings - String/Scalar Feature Extraction Module

This module extracts simple string and scalar features from CIA World Factbook data
for all countries. Unlike arrays and dictionaries, these are single-value fields
suitable for quick lookups and filtering.

Usage:
    from proj_004_cia.u_nation_feature_strings.extract_capital_string_per_country import get_capital

    capitals = get_capital()
    # Returns: {'USA': 'Washington, DC', 'FRA': 'Paris', ...}

Available Extractors:
    Government: capital, government_type, independence, national_holiday,
                national_symbol, suffrage, legal_system
    Geography: location, map_reference, terrain, time_zone, geographic_coordinates_text
    Society: nationality_noun, nationality_adjective
    Communications: internet_country_code, telephones_country_code
    Introduction: background (country overview)

Pattern:
    All extractors return Dict[str, str] mapping ISO3 codes to string values.
"""
