import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_06_economy.helper.utils.parse_econ_value import parse_econ_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_imports(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse imports data from CIA World Factbook for a given country.

    This parser extracts import data including:
    - Multi-year historical data
    - Latest value and year
    - Dollar values with estimate status
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured imports data:
        {
            "imports_data": [{"year": int, "value": float, "unit": str, "is_estimate": bool}],
            "imports_latest_value": float,
            "imports_latest_year": int,
            "imports_unit": str,
            "imports_note": str
        }

    Examples:
        >>> data = parse_imports('USA')
        >>> 'imports_latest_year' in data
        True

        >>> data = parse_imports('CHN')
        >>> isinstance(data.get('imports_data', []), list)
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Imports
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Imports', {})

    if return_original:
        return pass_data


    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        yearly_data = []
        for k, v in pass_data.items():
            if k == 'note':
                if isinstance(v, str) and v.strip():
                    result['imports_note'] = clean_text(v)
                continue
            if isinstance(v, dict) and 'text' in v:
                year_match = re.search(r'(\d{4})', k)
                if year_match:
                    year = int(year_match.group(1))
                    text = v.get('text', '')
                    if text:
                        parsed = parse_econ_value(text)
                        entry = {'year': year}
                        if parsed['value'] is not None:
                            entry['value'] = parsed['value']
                        if parsed['unit']:
                            entry['unit'] = parsed['unit']
                        if parsed['is_estimate']:
                            entry['is_estimate'] = parsed['is_estimate']
                        yearly_data.append(entry)
        if yearly_data:
            yearly_data.sort(key=lambda x: x['year'], reverse=True)
            result['imports_data'] = yearly_data
            if yearly_data[0].get('value') is not None:
                result['imports_latest_value'] = yearly_data[0]['value']
            result['imports_latest_year'] = yearly_data[0]['year']
            if yearly_data[0].get('unit'):
                result['imports_unit'] = yearly_data[0]['unit']
    except Exception as e:
        logger.error(f"Error parsing imports for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_imports with real country data."""
    print("="*60)
    print("Testing parse_imports across countries")
    print("="*60)

    test_countries = ['USA', 'CHN', 'IND', 'BRA', 'DEU', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_imports(iso3)

            if result.get('imports_latest_value') is not None:
                latest = result['imports_latest_value']
                year = result.get('imports_latest_year', '')
                unit = result.get('imports_unit', '$')

                # Format large numbers
                if latest >= 1e12:
                    display = f"${latest/1e12:.2f}T"
                elif latest >= 1e9:
                    display = f"${latest/1e9:.2f}B"
                elif latest >= 1e6:
                    display = f"${latest/1e6:.2f}M"
                else:
                    display = f"${latest:,.0f}"

                print(f"  Latest: {display} ({year})")

                if result.get('imports_data'):
                    data_count = len(result['imports_data'])
                    if data_count > 1:
                        print(f"  Historical data: {data_count} years")
                        # Show last 3 years
                        for entry in result['imports_data'][:3]:
                            val = entry.get('value', 'N/A')
                            yr = entry.get('year', '')
                            est = " (est.)" if entry.get('is_estimate') else ""
                            if isinstance(val, (int, float)):
                                if val >= 1e12:
                                    val_str = f"${val/1e12:.2f}T"
                                elif val >= 1e9:
                                    val_str = f"${val/1e9:.2f}B"
                                else:
                                    val_str = f"${val/1e6:.2f}M"
                            else:
                                val_str = str(val)
                            print(f"    {yr}: {val_str}{est}")
            else:
                print("  No imports data found")

            if result.get('imports_note'):
                note = result['imports_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
