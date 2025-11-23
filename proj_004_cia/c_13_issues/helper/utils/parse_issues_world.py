"""
Parse World-level transnational issues data from CIA World Factbook.
Extracts global statistics on refugees, trafficking tiers, and illicit drugs production.
"""
import re
import logging
from typing import Dict, Any, List
from bs4 import BeautifulSoup

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')

# ISO3 code mapping for trafficking tier countries
COUNTRY_TO_ISO3 = {
    "Afghanistan": "AFG", "Algeria": "DZA", "Belarus": "BLR", "Bolivia": "BOL",
    "Botswana": "BWA", "Brunei": "BRN", "Bulgaria": "BGR", "Burma": "MMR",
    "Cambodia": "KHM", "Chad": "TCD", "People's Republic of China": "CHN",
    "Cuba": "CUB", "Curacao": "CUW", "Djibouti": "DJI", "Dominican Republic": "DOM",
    "Egypt": "EGY", "El Salvador": "SLV", "Equatorial Guinea": "GNQ",
    "Eritrea": "ERI", "Eswatini": "SWZ", "Gabon": "GAB", "Guinea-Bissau": "GNB",
    "Haiti": "HTI", "Iran": "IRN", "Iraq": "IRQ", "Democratic People's Republic of Korea": "PRK",
    "Kuwait": "KWT", "Lebanon": "LBN", "Macau": "MAC", "Madagascar": "MDG",
    "Malaysia": "MYS", "Marshall Islands": "MHL", "Mauritius": "MUS",
    "Montenegro": "MNE", "Mozambique": "MOZ", "Nicaragua": "NIC",
    "Papua New Guinea": "PNG", "Republic of the Congo": "COG", "Russia": "RUS",
    "Serbia": "SRB", "Sint Maarten": "SXM", "Solomon Islands": "SLB",
    "South Africa": "ZAF", "South Sudan": "SSD", "Syria": "SYR",
    "Trinidad and Tobago": "TTO", "Turkmenistan": "TKM", "Vanuatu": "VUT",
    "Venezuela": "VEN", "Vietnam": "VNM"
}


def parse_issues_world(issues_data: dict, iso3Code: str = None) -> dict:
    """
    Parse World-level transnational issues data with detailed value extraction.

    Args:
        issues_data: Dict containing World transnational issues data

    Returns:
        Dict with extracted values:
            Refugees section:
                - displaced_total_value: int (total forcibly displaced worldwide)
                - displaced_total_year: int
                - idp_global_value: int (internally displaced persons)
                - refugees_global_value: int (refugees worldwide)
                - asylum_seekers_global_value: int
                - others_needing_protection_value: int
                - stateless_global_value: int

            Trafficking section:
                - tier_2_watchlist_count: int
                - tier_2_watchlist_countries: list of {name, iso3}
                - tier_2_watchlist_year: int
                - tier_3_count: int
                - tier_3_countries: list of {name, iso3}
                - tier_3_year: int

            Illicit drugs section:
                - coca_cultivation_hectares: int
                - coca_cultivation_year: int
                - cocaine_production_metric_tons: int
                - cocaine_production_year: int
                - opium_cultivation_hectares: int
                - opium_cultivation_year: int
                - opium_production_metric_tons: int
                - afghanistan_opium_share_percent: int
                - southeast_asia_opium_share_percent: int
                - latin_america_heroin_metric_tons: int
    """
    result = {}

    # Parse "Refugees and internally displaced persons"
    refugees_data = issues_data.get("Refugees and internally displaced persons", {})
    if refugees_data:
        text = refugees_data.get("text", "")
        if text:
            # Clean HTML
            soup = BeautifulSoup(text, "html.parser")
            clean_text = soup.get_text()

            # Extract total displaced: "110 million people forcibly displaced"
            total_match = re.search(r'([\d.]+)\s*million\s+people\s+forcibly\s+displaced', clean_text, re.IGNORECASE)
            if total_match:
                result["displaced_total_value"] = int(float(total_match.group(1)) * 1_000_000)

            # Extract year: "mid-year 2023"
            year_match = re.search(r'(?:mid-year|year-end|as of)\s+(\d{4})', clean_text, re.IGNORECASE)
            if year_match:
                result["displaced_total_year"] = int(year_match.group(1))

            # Extract IDPs: "62.5 million IDPs"
            idp_match = re.search(r'([\d.]+)\s*million\s+IDPs', clean_text, re.IGNORECASE)
            if idp_match:
                result["idp_global_value"] = int(float(idp_match.group(1)) * 1_000_000)

            # Extract refugees: "36.4 million refugees"
            refugees_match = re.search(r'([\d.]+)\s*million\s+refugees', clean_text, re.IGNORECASE)
            if refugees_match:
                result["refugees_global_value"] = int(float(refugees_match.group(1)) * 1_000_000)

            # Extract asylum seekers: "6.1 million asylum seekers"
            asylum_match = re.search(r'([\d.]+)\s*million\s+asylum\s+seekers', clean_text, re.IGNORECASE)
            if asylum_match:
                result["asylum_seekers_global_value"] = int(float(asylum_match.group(1)) * 1_000_000)

            # Extract others in need: "5.3 million others in need"
            others_match = re.search(r'([\d.]+)\s*million\s+others\s+in\s+need', clean_text, re.IGNORECASE)
            if others_match:
                result["others_needing_protection_value"] = int(float(others_match.group(1)) * 1_000_000)

            # Extract stateless: "4.4 million stateless persons"
            stateless_match = re.search(r'([\d.]+)\s*million\s+stateless', clean_text, re.IGNORECASE)
            if stateless_match:
                result["stateless_global_value"] = int(float(stateless_match.group(1)) * 1_000_000)

    # Parse "Trafficking in persons"
    trafficking_data = issues_data.get("Trafficking in persons", {})
    if trafficking_data:
        tier_data = trafficking_data.get("tier rating", {})
        text = tier_data.get("text", "")
        if text:
            # Clean HTML
            soup = BeautifulSoup(text, "html.parser")
            clean_text = soup.get_text()

            # Parse Tier 2 Watch List
            tier2_match = re.search(
                r'Tier\s+2\s+Watch\s+List[:\s]*\((\d+)\s+countries\)\s*(.+?)(?=Tier\s+3|$)',
                clean_text, re.IGNORECASE | re.DOTALL
            )
            if tier2_match:
                result["tier_2_watchlist_count"] = int(tier2_match.group(1))
                countries_str = tier2_match.group(2)

                # Extract year from countries section
                year_match = re.search(r'\((\d{4})\)', countries_str)
                if year_match:
                    result["tier_2_watchlist_year"] = int(year_match.group(1))
                    countries_str = countries_str[:countries_str.rfind('(')]

                # Parse country names
                countries = []
                for country in countries_str.split(','):
                    country = country.strip()
                    if country and not country.isdigit():
                        countries.append({
                            "name": country,
                            "iso3": COUNTRY_TO_ISO3.get(country, None)
                        })
                result["tier_2_watchlist_countries"] = countries

            # Parse Tier 3
            tier3_match = re.search(
                r'Tier\s+3[:\s]*\((\d+)\s+countries\)\s*(.+?)(?:\((\d{4})\))?$',
                clean_text, re.IGNORECASE | re.DOTALL
            )
            if tier3_match:
                result["tier_3_count"] = int(tier3_match.group(1))
                countries_str = tier3_match.group(2)

                # Extract year
                year_match = re.search(r'\((\d{4})\)', countries_str)
                if year_match:
                    result["tier_3_year"] = int(year_match.group(1))
                    countries_str = re.sub(r'\(\d{4}\)', '', countries_str)

                # Parse country names
                countries = []
                for country in countries_str.split(','):
                    country = country.strip()
                    if country and not country.isdigit():
                        countries.append({
                            "name": country,
                            "iso3": COUNTRY_TO_ISO3.get(country, None)
                        })
                result["tier_3_countries"] = countries

    # Parse "Illicit drugs"
    drugs_data = issues_data.get("Illicit drugs", {})
    if drugs_data:
        text = drugs_data.get("text", "")
        if text:
            # Clean HTML
            soup = BeautifulSoup(text, "html.parser")
            clean_text = soup.get_text()

            # Coca cultivation: "373,000 hectares"
            coca_match = re.search(r'coca\s+cultivation[^:]*?(\d{4})[^:]*?([\d,]+)\s*hectares', clean_text, re.IGNORECASE)
            if not coca_match:
                coca_match = re.search(r'([\d,]+)\s*hectares.*?coca.*?(\d{4})', clean_text, re.IGNORECASE)
            if coca_match:
                # Handle both orderings
                if coca_match.group(1).replace(',', '').isdigit() and len(coca_match.group(1)) > 4:
                    result["coca_cultivation_hectares"] = int(coca_match.group(1).replace(',', ''))
                    result["coca_cultivation_year"] = int(coca_match.group(2))
                else:
                    result["coca_cultivation_year"] = int(coca_match.group(1))
                    result["coca_cultivation_hectares"] = int(coca_match.group(2).replace(',', ''))

            # Alternative pattern for coca
            if "coca_cultivation_hectares" not in result:
                coca_alt = re.search(r'coca\s+cultivation.*?([\d,]+)\s*hectares', clean_text, re.IGNORECASE)
                if coca_alt:
                    result["coca_cultivation_hectares"] = int(coca_alt.group(1).replace(',', ''))

            # Cocaine production: "2,100 metric tons"
            cocaine_match = re.search(r'cocaine\s+production[^:]*?([\d,]+)\s*metric\s*t', clean_text, re.IGNORECASE)
            if not cocaine_match:
                cocaine_match = re.search(r'([\d,]+)\s*metric\s*t[^\d]*cocaine', clean_text, re.IGNORECASE)
            if cocaine_match:
                result["cocaine_production_metric_tons"] = int(cocaine_match.group(1).replace(',', ''))

            # Extract year for cocaine (usually same as coca)
            cocaine_year = re.search(r'cocaine[^(]*\((\d{4})\)', clean_text, re.IGNORECASE)
            if not cocaine_year:
                cocaine_year = re.search(r'in\s+(\d{4})', clean_text[:clean_text.lower().find('opiate') if 'opiate' in clean_text.lower() else len(clean_text)])
            if cocaine_year:
                result["cocaine_production_year"] = int(cocaine_year.group(1))

            # Opium poppy: "265,000 hectares"
            opium_match = re.search(r'opium\s+poppy\s+cultivation[^:]*?([\d,]+)\s*hectares', clean_text, re.IGNORECASE)
            if not opium_match:
                opium_match = re.search(r'([\d,]+)\s*hectares.*?opium', clean_text, re.IGNORECASE)
            if opium_match:
                result["opium_cultivation_hectares"] = int(opium_match.group(1).replace(',', ''))

            # Opium production: "7,300 metric tons"
            opium_prod = re.search(r'opium\s+production[^:]*?([\d,]+)\s*metric\s*t', clean_text, re.IGNORECASE)
            if not opium_prod:
                opium_prod = re.search(r'([\d,]+)\s*metric\s*t[^\d]*opium', clean_text, re.IGNORECASE)
            if opium_prod:
                result["opium_production_metric_tons"] = int(opium_prod.group(1).replace(',', ''))

            # Afghanistan share: "85% of the global supply"
            afg_match = re.search(r'Afghanistan[^%]*?(\d+)%', clean_text, re.IGNORECASE)
            if afg_match:
                result["afghanistan_opium_share_percent"] = int(afg_match.group(1))

            # Southeast Asia share: "7% of global opium"
            sea_match = re.search(r'Southeast\s+Asia[^%]*?(\d+)%', clean_text, re.IGNORECASE)
            if sea_match:
                result["southeast_asia_opium_share_percent"] = int(sea_match.group(1))

            # Latin America heroin: "61 metric tons"
            la_match = re.search(r'Latin\s+America[^:]*?(\d+)\s*metric\s*t', clean_text, re.IGNORECASE)
            if la_match:
                result["latin_america_heroin_metric_tons"] = int(la_match.group(1))

            # Extract year for drugs data: "(2015)" at end
            drugs_year = re.search(r'\((\d{4})\)\s*$', clean_text)
            if drugs_year:
                result["illicit_drugs_year"] = int(drugs_year.group(1))

    return result


# Example usage
if __name__ == "__main__":
    test_data = {
        "Refugees and internally displaced persons": {
            "text": "<p>the UN High Commissioner for Refugees (UNHCR) estimated that as of mid-year 2023 there were 110 million people forcibly displaced worldwide; this includes 62.5 million IDPs, 36.4 million refugees, 6.1 million asylum seekers, 5.3 million others in need of international protection; the UNHCR estimates there are currently more than 4.4 million stateless persons as of year-end 2022</p>"
        },
        "Trafficking in persons": {
            "tier rating": {
                "text": "<strong>Tier 2 Watch List:</strong> (26 countries) Bolivia, Botswana, Brunei, Bulgaria (2023)<br><br><strong>Tier 3:</strong> (24 countries) Afghanistan, Algeria, Belarus (2023)"
            }
        },
        "Illicit drugs": {
            "text": "<p><strong>cocaine:</strong> worldwide coca cultivation in 2020 likely amounted to 373,000 hectares, potential pure cocaine production reached 2,100 metric tons in 2020<br><strong>opiates:</strong> worldwide illicit opium poppy cultivation probably reached about 265,000 hectares in 2020, with potential opium production reaching 7,300 metric tons; Afghanistan is world's primary opium producer, accounting for 85% of the global supply; Southeast Asia was responsible for 7% of global opium; Latin America opium in 2020 was sufficient to produce about 61 metric tons of pure heroin</p> (2015)"
        }
    }
    parsed = parse_issues_world(test_data, "WLD")
    from pprint import pprint
    pprint(parsed)
