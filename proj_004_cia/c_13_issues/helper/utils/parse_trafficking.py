import re
import logging
from bs4 import BeautifulSoup
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Example mapping of country names to ISO 3 codes
country_to_iso3 = {
    "Bolivia": "BOL",
    "Botswana": "BWA",
    "Brunei": "BRN",
    "Bulgaria": "BGR",
    "Republic of the Congo": "COG",
    "Dominican Republic": "DOM",
    "Egypt": "EGY",
    "El Salvador": "SLV",
    "Eswatini": "SWZ",
    "Gabon": "GAB",
    "Haiti": "HTI",
    "Iraq": "IRQ",
    "Kuwait": "KWT",
    "Lebanon": "LBN",
    "Madagascar": "MDG",
    "Malaysia": "MYS",
    "Marshall Islands": "MHL",
    "Mauritius": "MUS",
    "Montenegro": "MNE",
    "Mozambique": "MOZ",
    "Serbia": "SRB",
    "Solomon Islands": "SLB",
    "South Africa": "ZAF",
    "Trinidad and Tobago": "TTO",
    "Vanuatu": "VUT",
    "Vietnam": "VNM",
    "Afghanistan": "AFG",
    "Algeria": "DZA",
    "Belarus": "BLR",
    "Burma": "MMR",
    "Cambodia": "KHM",
    "Chad": "TCD",
    "People's Republic of China": "CHN",
    "Cuba": "CUB",
    "Curacao": "CUW",
    "Djibouti": "DJI",
    "Equatorial Guinea": "GNQ",
    "Eritrea": "ERI",
    "Guinea-Bissau": "GNB",
    "Iran": "IRN",
    "Democratic People's Republic of Korea": "PRK",
    "Macau": "MAC",
    "Nicaragua": "NIC",
    "Papua New Guinea": "PNG",
    "Russia": "RUS",
    "Sint Maarten": "SXM",
    "South Sudan": "SSD",
    "Syria": "SYR",
    "Turkmenistan": "TKM",
    "Venezuela": "VEN"
}

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_trafficking(traffick_data: dict, iso3Code: str = None) -> dict:
    """
    Parses data related to trafficking in persons, including tier ratings and additional descriptions.

    Parameters:
        traffick_data (dict): The dictionary containing trafficking in persons data.
        iso3Code (str): ISO 3 country code.

    Returns:
        dict: A dictionary containing parsed information for tier rating.
    """
    result = {
        "tier_rating": []
    }

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
                    # Use 'N/A' if the ISO code is not found
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

    return result


# Example usage
if __name__ == "__main__":
    # Example 1: World Data
    traffick_data_world = {
        "tier rating": {
            "text": "<strong><br><br>Tier 2 Watch List:</strong> (26 countries) Bolivia, Botswana, Brunei, Bulgaria, Republic of the Congo, Dominican Republic, Egypt, El Salvador, Eswatini, Gabon, Haiti, Iraq, Kuwait, Lebanon, Madagascar, Malaysia, Marshall Islands, Mauritius, Montenegro, Mozambique, Serbia, Solomon Islands, South Africa, Trinidad and Tobago, Vanuatu, Vietnam (2023)<br><br><strong>Tier 3:</strong> (24 countries) Afghanistan, Algeria, Belarus, Burma, Cambodia, Chad, People's Republic of China, Cuba, Curacao, Djibouti, Equatorial Guinea, Eritrea, Guinea-Bissau, Iran, Democratic People's Republic of Korea, Macau, Nicaragua, Papua New Guinea, Russia, Sint Maarten, South Sudan, Syria, Turkmenistan, Venezuela (2023)"
        }
    }
    parsed_data_world = parse_trafficking(traffick_data_world, iso3Code="WLD")
    print(parsed_data_world)

    # Example 2: Individual Country Data
    traffick_data_country = {
        "tier rating": {
            "text": "Tier 2 Watch list — Algeria does not fully meet the minimum standards for the elimination of trafficking but is making significant efforts to do so, therefore Algeria was upgraded to Tier 2 Watch List; for more details, go to: https://www.state.gov/reports/2024-trafficking-in-persons-report/algeria/"
        }
    }
    parsed_data_country = parse_trafficking(
        traffick_data_country, iso3Code="DZA")
    print(parsed_data_country)
