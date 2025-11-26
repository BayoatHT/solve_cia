import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_budget(budget_data: dict, iso3Code: str = None, return_original: bool = False) -> dict:
    """
    Parse budget data from CIA World Factbook for a given country.

    This parser extracts government budget information including:
    - Revenues (value, year)
    - Expenditures (value, year)
    - Handles multiple numeric formats (trillion, billion, million)
    - Fiscal year notation support

    Args:
        budget_data: The 'Budget' section from the Economy data
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')
        return_original: If True, return the raw data without parsing

    Returns:
        Dictionary with structured budget data:
        {
            "budget_revenues": {"value": float, "unit": "$", "date": str},
            "budget_expenditures": {"value": float, "unit": "$", "date": str}
        }

    Examples:
        >>> data = parse_budget({'revenues': {'text': '$6.429 trillion (2019 est.)'}}, 'USA')
        >>> data['budget_revenues']['value'] > 0
        True
    """
    result = {}

    if return_original:
        return budget_data

    if not budget_data or not isinstance(budget_data, dict):
        return {
            "budget_revenues": {"value": None, "unit": "$", "date": ""},
            "budget_expenditures": {"value": None, "unit": "$", "date": ""}
        }

    # Define mapping for keys
    budget_keys = {
        "revenues": "budget_revenues",
        "expenditures": "budget_expenditures"
    }

    for key, result_key in budget_keys.items():
        item = budget_data.get(key, {}).get("text", "")

        # Define default values for result
        result[result_key] = {"value": 0, "unit": "$", "date": ""}

        # Skip NA values
        if item.upper().strip() == 'NA':
            result[result_key]["value"] = None
            result[result_key]["note"] = "NA"
            continue

        # Try multiple patterns
        # Pattern 1: $X.XXX trillion/billion/million (YYYY est.)
        match = re.match(r"\$([\d,.]+)\s+(trillion|billion|million)\s+\((\d{4})\s+est\.\)", item)
        if match:
            value_str = match.group(1).replace(",", "")
            unit = match.group(2)
            year = match.group(3)
            multipliers = {"trillion": 1e12, "billion": 1e9, "million": 1e6}
            result[result_key]["value"] = float(value_str) * multipliers.get(unit, 1)
            result[result_key]["date"] = year
            continue

        # Pattern 2: $X.XXX trillion/billion/million (YYYY) - without "est."
        match = re.match(r"\$([\d,.]+)\s+(trillion|billion|million)\s+\((\d{4})\)", item)
        if match:
            value_str = match.group(1).replace(",", "")
            unit = match.group(2)
            year = match.group(3)
            multipliers = {"trillion": 1e12, "billion": 1e9, "million": 1e6}
            result[result_key]["value"] = float(value_str) * multipliers.get(unit, 1)
            result[result_key]["date"] = year
            continue

        # Pattern 3: $X.XXX million (FYXX/XX est.) - fiscal year format
        match = re.match(r"\$([\d,.]+)\s+(trillion|billion|million)\s+\(FY\d{2}/\d{2}(?:\s+est\.)?\)", item)
        if match:
            value_str = match.group(1).replace(",", "")
            unit = match.group(2)
            multipliers = {"trillion": 1e12, "billion": 1e9, "million": 1e6}
            result[result_key]["value"] = float(value_str) * multipliers.get(unit, 1)
            result[result_key]["date"] = ""  # Don't extract FY format
            continue

        # Pattern 4: $X,XXX,XXX (YYYY est.) - raw numbers with commas
        match = re.match(r"\$([\d,]+)\s+\((\d{4})\s+est\.\)", item)
        if match:
            value_str = match.group(1).replace(",", "")
            year = match.group(2)
            result[result_key]["value"] = float(value_str)
            result[result_key]["date"] = year
            continue

        # Pattern 5: Just the raw value without year
        match = re.match(r"\$([\d,.]+)\s+(trillion|billion|million)", item)
        if match:
            value_str = match.group(1).replace(",", "")
            unit = match.group(2)
            multipliers = {"trillion": 1e12, "billion": 1e9, "million": 1e6}
            result[result_key]["value"] = float(value_str) * multipliers.get(unit, 1)
            continue

        # If no pattern matches, log warning
        if item:
            logger.warning(f"Could not parse budget item for {iso3Code}: {item[:50]}")

    return result


if __name__ == "__main__":
    """Test parse_budget with real country data."""
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

    print("="*60)
    print("Testing parse_budget across countries")
    print("="*60)

    test_countries = ['USA', 'CHN', 'IND', 'BRA', 'DEU', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            raw_data = load_country_data(iso3)
            budget_data = raw_data.get('Economy', {}).get('Budget', {})
            result = parse_budget(budget_data, iso3)

            for key in ['budget_revenues', 'budget_expenditures']:
                data = result.get(key, {})
                value = data.get('value')
                date = data.get('date', '')

                if value is not None:
                    # Format large numbers
                    if value >= 1e12:
                        display = f"${value/1e12:.2f}T"
                    elif value >= 1e9:
                        display = f"${value/1e9:.2f}B"
                    elif value >= 1e6:
                        display = f"${value/1e6:.2f}M"
                    else:
                        display = f"${value:,.0f}"

                    year_str = f" ({date})" if date else ""
                    print(f"  {key}: {display}{year_str}")
                else:
                    print(f"  {key}: N/A")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
