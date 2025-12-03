"""
ISO Country Code Mapping for World Heritage Sites.

UNESCO World Heritage data uses ISO2 codes, but our system uses ISO3 codes.
This module provides complete bidirectional mapping for all 170 countries
in the heritage dataset.
"""

from typing import Dict, Optional

# ISO2 to ISO3 mapping (170 countries in World Heritage dataset)
ISO2_TO_ISO3: Dict[str, str] = {
    'AD': 'AND', 'AE': 'ARE', 'AF': 'AFG', 'AG': 'ATG', 'AL': 'ALB',
    'AM': 'ARM', 'AO': 'AGO', 'AR': 'ARG', 'AT': 'AUT', 'AU': 'AUS',
    'AZ': 'AZE', 'BA': 'BIH', 'BB': 'BRB', 'BD': 'BGD', 'BE': 'BEL',
    'BF': 'BFA', 'BG': 'BGR', 'BH': 'BHR', 'BJ': 'BEN', 'BO': 'BOL',
    'BR': 'BRA', 'BW': 'BWA', 'BY': 'BLR', 'BZ': 'BLZ', 'CA': 'CAN',
    'CD': 'COD', 'CF': 'CAF', 'CG': 'COG', 'CH': 'CHE', 'CI': 'CIV',
    'CL': 'CHL', 'CM': 'CMR', 'CN': 'CHN', 'CO': 'COL', 'CR': 'CRI',
    'CU': 'CUB', 'CV': 'CPV', 'CY': 'CYP', 'CZ': 'CZE', 'DE': 'DEU',
    'DK': 'DNK', 'DM': 'DMA', 'DO': 'DOM', 'DZ': 'DZA', 'EC': 'ECU',
    'EE': 'EST', 'EG': 'EGY', 'ER': 'ERI', 'ES': 'ESP', 'ET': 'ETH',
    'FI': 'FIN', 'FJ': 'FJI', 'FM': 'FSM', 'FR': 'FRA', 'GA': 'GAB',
    'GB': 'GBR', 'GE': 'GEO', 'GH': 'GHA', 'GM': 'GMB', 'GN': 'GIN',
    'GR': 'GRC', 'GT': 'GTM', 'GW': 'GNB', 'HN': 'HND', 'HR': 'HRV',
    'HT': 'HTI', 'HU': 'HUN', 'ID': 'IDN', 'IE': 'IRL', 'IL': 'ISR',
    'IN': 'IND', 'IQ': 'IRQ', 'IR': 'IRN', 'IS': 'ISL', 'IT': 'ITA',
    'JM': 'JAM', 'JO': 'JOR', 'JP': 'JPN', 'KE': 'KEN', 'KG': 'KGZ',
    'KH': 'KHM', 'KI': 'KIR', 'KN': 'KNA', 'KP': 'PRK', 'KR': 'KOR',
    'KZ': 'KAZ', 'LA': 'LAO', 'LB': 'LBN', 'LC': 'LCA', 'LK': 'LKA',
    'LS': 'LSO', 'LT': 'LTU', 'LU': 'LUX', 'LV': 'LVA', 'LY': 'LBY',
    'MA': 'MAR', 'MD': 'MDA', 'ME': 'MNE', 'MG': 'MDG', 'MH': 'MHL',
    'MK': 'MKD', 'ML': 'MLI', 'MM': 'MMR', 'MN': 'MNG', 'MR': 'MRT',
    'MT': 'MLT', 'MU': 'MUS', 'MW': 'MWI', 'MX': 'MEX', 'MY': 'MYS',
    'MZ': 'MOZ', 'NA': 'NAM', 'NE': 'NER', 'NG': 'NGA', 'NI': 'NIC',
    'NL': 'NLD', 'NO': 'NOR', 'NP': 'NPL', 'NZ': 'NZL', 'OM': 'OMN',
    'PA': 'PAN', 'PE': 'PER', 'PG': 'PNG', 'PH': 'PHL', 'PK': 'PAK',
    'PL': 'POL', 'PS': 'PSE', 'PT': 'PRT', 'PW': 'PLW', 'PY': 'PRY',
    'QA': 'QAT', 'RO': 'ROU', 'RS': 'SRB', 'RU': 'RUS', 'RW': 'RWA',
    'SA': 'SAU', 'SB': 'SLB', 'SC': 'SYC', 'SD': 'SDN', 'SE': 'SWE',
    'SG': 'SGP', 'SI': 'SVN', 'SK': 'SVK', 'SL': 'SLE', 'SM': 'SMR',
    'SN': 'SEN', 'SR': 'SUR', 'SV': 'SLV', 'SY': 'SYR', 'TD': 'TCD',
    'TG': 'TGO', 'TH': 'THA', 'TJ': 'TJK', 'TM': 'TKM', 'TN': 'TUN',
    'TR': 'TUR', 'TZ': 'TZA', 'UA': 'UKR', 'UG': 'UGA', 'US': 'USA',
    'UY': 'URY', 'UZ': 'UZB', 'VA': 'VAT', 'VE': 'VEN', 'VN': 'VNM',
    'VU': 'VUT', 'YE': 'YEM', 'ZA': 'ZAF', 'ZM': 'ZMB', 'ZW': 'ZWE',
}

# Reverse mapping: ISO3 to ISO2
ISO3_TO_ISO2: Dict[str, str] = {v: k for k, v in ISO2_TO_ISO3.items()}

# ISO3 to country name mapping
ISO3_TO_COUNTRY_NAME: Dict[str, str] = {
    'AFG': 'Afghanistan', 'AGO': 'Angola', 'ALB': 'Albania', 'AND': 'Andorra',
    'ARE': 'United Arab Emirates', 'ARG': 'Argentina', 'ARM': 'Armenia',
    'ATG': 'Antigua and Barbuda', 'AUS': 'Australia', 'AUT': 'Austria',
    'AZE': 'Azerbaijan', 'BEL': 'Belgium', 'BEN': 'Benin', 'BFA': 'Burkina Faso',
    'BGD': 'Bangladesh', 'BGR': 'Bulgaria', 'BHR': 'Bahrain',
    'BIH': 'Bosnia and Herzegovina', 'BLR': 'Belarus', 'BLZ': 'Belize',
    'BOL': 'Bolivia', 'BRA': 'Brazil', 'BRB': 'Barbados', 'BWA': 'Botswana',
    'CAF': 'Central African Republic', 'CAN': 'Canada', 'CHE': 'Switzerland',
    'CHL': 'Chile', 'CHN': 'China', 'CIV': "Côte d'Ivoire", 'CMR': 'Cameroon',
    'COD': 'Democratic Republic of the Congo', 'COG': 'Congo', 'COL': 'Colombia',
    'CPV': 'Cabo Verde', 'CRI': 'Costa Rica', 'CUB': 'Cuba', 'CYP': 'Cyprus',
    'CZE': 'Czechia', 'DEU': 'Germany', 'DMA': 'Dominica', 'DNK': 'Denmark',
    'DOM': 'Dominican Republic', 'DZA': 'Algeria', 'ECU': 'Ecuador',
    'EGY': 'Egypt', 'ERI': 'Eritrea', 'ESP': 'Spain', 'EST': 'Estonia',
    'ETH': 'Ethiopia', 'FIN': 'Finland', 'FJI': 'Fiji', 'FRA': 'France',
    'FSM': 'Micronesia', 'GAB': 'Gabon', 'GBR': 'United Kingdom',
    'GEO': 'Georgia', 'GHA': 'Ghana', 'GIN': 'Guinea', 'GMB': 'Gambia',
    'GNB': 'Guinea-Bissau', 'GRC': 'Greece', 'GTM': 'Guatemala',
    'HND': 'Honduras', 'HRV': 'Croatia', 'HTI': 'Haiti', 'HUN': 'Hungary',
    'IDN': 'Indonesia', 'IND': 'India', 'IRL': 'Ireland', 'IRN': 'Iran',
    'IRQ': 'Iraq', 'ISL': 'Iceland', 'ISR': 'Israel', 'ITA': 'Italy',
    'JAM': 'Jamaica', 'JOR': 'Jordan', 'JPN': 'Japan', 'KAZ': 'Kazakhstan',
    'KEN': 'Kenya', 'KGZ': 'Kyrgyzstan', 'KHM': 'Cambodia', 'KIR': 'Kiribati',
    'KNA': 'Saint Kitts and Nevis', 'KOR': 'South Korea', 'LAO': 'Laos',
    'LBN': 'Lebanon', 'LBY': 'Libya', 'LCA': 'Saint Lucia', 'LKA': 'Sri Lanka',
    'LSO': 'Lesotho', 'LTU': 'Lithuania', 'LUX': 'Luxembourg', 'LVA': 'Latvia',
    'MAR': 'Morocco', 'MDA': 'Moldova', 'MDG': 'Madagascar', 'MEX': 'Mexico',
    'MHL': 'Marshall Islands', 'MKD': 'North Macedonia', 'MLI': 'Mali',
    'MLT': 'Malta', 'MMR': 'Myanmar', 'MNE': 'Montenegro', 'MNG': 'Mongolia',
    'MOZ': 'Mozambique', 'MRT': 'Mauritania', 'MUS': 'Mauritius',
    'MWI': 'Malawi', 'MYS': 'Malaysia', 'NAM': 'Namibia', 'NER': 'Niger',
    'NGA': 'Nigeria', 'NIC': 'Nicaragua', 'NLD': 'Netherlands', 'NOR': 'Norway',
    'NPL': 'Nepal', 'NZL': 'New Zealand', 'OMN': 'Oman', 'PAK': 'Pakistan',
    'PAN': 'Panama', 'PER': 'Peru', 'PHL': 'Philippines', 'PLW': 'Palau',
    'PNG': 'Papua New Guinea', 'POL': 'Poland', 'PRK': 'North Korea',
    'PRT': 'Portugal', 'PRY': 'Paraguay', 'PSE': 'Palestine', 'QAT': 'Qatar',
    'ROU': 'Romania', 'RUS': 'Russia', 'RWA': 'Rwanda', 'SAU': 'Saudi Arabia',
    'SDN': 'Sudan', 'SEN': 'Senegal', 'SGP': 'Singapore',
    'SLB': 'Solomon Islands', 'SLE': 'Sierra Leone', 'SLV': 'El Salvador',
    'SMR': 'San Marino', 'SRB': 'Serbia', 'SUR': 'Suriname', 'SVK': 'Slovakia',
    'SVN': 'Slovenia', 'SWE': 'Sweden', 'SYC': 'Seychelles', 'SYR': 'Syria',
    'TCD': 'Chad', 'TGO': 'Togo', 'THA': 'Thailand', 'TJK': 'Tajikistan',
    'TKM': 'Turkmenistan', 'TUN': 'Tunisia', 'TUR': 'Turkey', 'TZA': 'Tanzania',
    'UGA': 'Uganda', 'UKR': 'Ukraine', 'URY': 'Uruguay', 'USA': 'United States',
    'UZB': 'Uzbekistan', 'VAT': 'Vatican City', 'VEN': 'Venezuela',
    'VNM': 'Vietnam', 'VUT': 'Vanuatu', 'YEM': 'Yemen', 'ZAF': 'South Africa',
    'ZMB': 'Zambia', 'ZWE': 'Zimbabwe',
}


def convert_iso2_to_iso3(iso2_code: str) -> Optional[str]:
    """
    Convert ISO2 country code to ISO3.

    Args:
        iso2_code: Two-letter ISO country code (e.g., 'FR')

    Returns:
        Three-letter ISO3 code (e.g., 'FRA') or None if not found

    Example:
        >>> convert_iso2_to_iso3('FR')
        'FRA'
    """
    return ISO2_TO_ISO3.get(iso2_code.upper())


def convert_iso3_to_iso2(iso3_code: str) -> Optional[str]:
    """
    Convert ISO3 country code to ISO2.

    Args:
        iso3_code: Three-letter ISO country code (e.g., 'FRA')

    Returns:
        Two-letter ISO2 code (e.g., 'FR') or None if not found

    Example:
        >>> convert_iso3_to_iso2('FRA')
        'FR'
    """
    return ISO3_TO_ISO2.get(iso3_code.upper())


def get_country_info(iso2_code: str) -> Optional[Dict[str, str]]:
    """
    Get complete country information from ISO2 code.

    Args:
        iso2_code: Two-letter ISO country code

    Returns:
        Dictionary with iso2, iso3, and name, or None if not found

    Example:
        >>> get_country_info('FR')
        {'iso2': 'FR', 'iso3': 'FRA', 'name': 'France'}
    """
    iso2_code = iso2_code.upper()
    iso3_code = ISO2_TO_ISO3.get(iso2_code)

    if not iso3_code:
        return None

    return {
        'iso2': iso2_code,
        'iso3': iso3_code,
        'name': ISO3_TO_COUNTRY_NAME.get(iso3_code, 'Unknown')
    }


def parse_iso_codes_string(iso_codes_str: str) -> list:
    """
    Parse comma-separated ISO2 codes to list of ISO3 codes.

    Args:
        iso_codes_str: Comma-separated ISO2 codes (e.g., "FR, DE, IT")

    Returns:
        List of ISO3 codes (e.g., ['FRA', 'DEU', 'ITA'])

    Example:
        >>> parse_iso_codes_string("FR, DE, IT")
        ['FRA', 'DEU', 'ITA']
    """
    iso2_codes = [code.strip().upper() for code in iso_codes_str.split(',')]
    iso3_codes = []

    for iso2 in iso2_codes:
        iso3 = ISO2_TO_ISO3.get(iso2)
        if iso3:
            iso3_codes.append(iso3)

    return iso3_codes
