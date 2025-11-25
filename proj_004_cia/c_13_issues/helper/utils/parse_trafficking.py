import re
import logging
from bs4 import BeautifulSoup
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Example mapping of country names to ISO 3 codes
country_to_iso3 = {
    "Bolivia": "BOL", "Botswana": "BWA", "Brunei": "BRN", "Bulgaria": "BGR",
    "Republic of the Congo": "COG", "Dominican Republic": "DOM", "Egypt": "EGY",
    "El Salvador": "SLV", "Eswatini": "SWZ", "Gabon": "GAB", "Haiti": "HTI",
    "Iraq": "IRQ", "Kuwait": "KWT", "Lebanon": "LBN", "Madagascar": "MDG",
    "Malaysia": "MYS", "Marshall Islands": "MHL", "Mauritius": "MUS",
    "Montenegro": "MNE", "Mozambique": "MOZ", "Serbia": "SRB",
    "Solomon Islands": "SLB", "South Africa": "ZAF", "Trinidad and Tobago": "TTO",
    "Vanuatu": "VUT", "Vietnam": "VNM", "Afghanistan": "AFG", "Algeria": "DZA",
    "Belarus": "BLR", "Burma": "MMR", "Cambodia": "KHM", "Chad": "TCD",
    "People's Republic of China": "CHN", "Cuba": "CUB", "Curacao": "CUW",
    "Djibouti": "DJI", "Equatorial Guinea": "GNQ", "Eritrea": "ERI",
    "Guinea-Bissau": "GNB", "Iran": "IRN", "Democratic People's Republic of Korea": "PRK",
    "Macau": "MAC", "Nicaragua": "NIC", "Papua New Guinea": "PNG", "Russia": "RUS",
    "Sint Maarten": "SXM", "South Sudan": "SSD", "Syria": "SYR",
    "Turkmenistan": "TKM", "Venezuela": "VEN"
}


def parse_trafficking(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse trafficking in persons data from CIA Transnational Issues section.

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'WLD')

    Returns:
        dict: A dictionary containing parsed information for tier rating.
    """
    result = {
        "tier_rating": []
    }

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    issues_section = raw_data.get('Transnational Issues', {})
    traffick_data = issues_section.get('Trafficking in persons', {})

    if return_original:
        return traffick_data


    if not traffick_data or not isinstance(traffick_data, dict):
        return result

    try:
        # Handle 'tier rating'
        tier_data = traffick_data.get("tier rating", {}).get("text", "")
        if not tier_data:
            return result

        if iso3Code == "WLD":
            # Clean HTML tags using BeautifulSoup
            soup = BeautifulSoup(tier_data, "html.parser")
            cleaned_text = soup.get_text(separator=" ")

            # Regular expression to match tiers and extract tier, countries, and year
            tier_pattern = re.compile(
                r"(Tier \d(?: Watch List)?)\s*:\s*\((\d+) countries\)\s*(.*?)(\(\d{4}\))")
            matches = tier_pattern.findall(cleaned_text)

            for match in matches:
                tier, _, countries_str, year_str = match
                year = int(year_str.strip("()"))

                # Split the countries string and clean them
                countries = [country.strip()
                             for country in countries_str.split(",") if country.strip()]

                # Generate list of country dictionaries with name and ISO 3 code
                countries_with_iso3 = [
                    {
                        "name": country,
                        "iso3": country_to_iso3.get(country, "N/A")
                    }
                    for country in countries
                ]

                # Append parsed information to the result
                result["tier_rating"].append({
                    "tier": tier,
                    "countries": countries_with_iso3,
                    "year": year
                })

        else:
            # For individual countries, parse tier rating and description
            # Split the text at the hyphen to separate the tier rating and description
            parts = tier_data.split('—', 1)
            tier_info = {
                "tier": clean_text(parts[0].strip()) if len(parts) > 0 else "",
                "description": clean_text(parts[1].strip()) if len(parts) > 1 else ""
            }
            result["tier_rating"].append(tier_info)

    except Exception as e:
        logger.error(f"Error parsing trafficking for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Testing parse_trafficking")
    print("=" * 60)
    for iso3 in ['USA', 'DEU', 'THA', 'NGA', 'RUS', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_trafficking(iso3)
            if result.get('tier_rating'):
                for tier in result['tier_rating'][:2]:
                    if 'countries' in tier:
                        print(f"  {tier['tier']}: {len(tier['countries'])} countries")
                    else:
                        tier_val = tier.get('tier', 'N/A')[:40]
                        print(f"  Tier: {tier_val}...")
            else:
                print("  No trafficking data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "=" * 60)
    print("✓ Tests complete")
