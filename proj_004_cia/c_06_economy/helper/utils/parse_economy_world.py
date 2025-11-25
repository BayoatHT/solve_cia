"""
Parse World-level economy data from CIA World Factbook.
Extracts global GDP, labor force, top agricultural products, etc.
"""
import re
import logging
from typing import Dict, Any, List
from bs4 import BeautifulSoup

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_economy_world(econ_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parse World-level economy data with detailed value extraction.

    Returns:
        Dict with:
            - gdp_official_value: float (in trillions USD)
            - gdp_official_year: int
            - labor_force_value: float (in billions)
            - labor_force_year: int
            - top_agricultural_products: list
            - industrial_production_growth_rate: float
    """
    if return_original:
        return econ_data

    result = {}

    # Parse "GDP (official exchange rate)"
    gdp_data = econ_data.get("GDP (official exchange rate)", {})
    if gdp_data:
        text = gdp_data.get("text", "")
        if text:
            # Match "$105.435 trillion (2023 est.)"
            match = re.search(r'\$([\d.]+)\s*(trillion|billion)', text, re.IGNORECASE)
            if match:
                value = float(match.group(1))
                magnitude = match.group(2).lower()
                if magnitude == 'trillion':
                    result['gdp_official_value_trillion_usd'] = value
                elif magnitude == 'billion':
                    result['gdp_official_value_trillion_usd'] = value / 1000

            year_match = re.search(r'\((\d{4})', text)
            if year_match:
                result['gdp_official_year'] = int(year_match.group(1))

    # Parse "Labor force"
    labor_data = econ_data.get("Labor force", {})
    if labor_data:
        text = labor_data.get("text", "")
        if text:
            # Match "3.628 billion (2023 est.)"
            match = re.search(r'([\d.]+)\s*(billion|million)', text, re.IGNORECASE)
            if match:
                value = float(match.group(1))
                magnitude = match.group(2).lower()
                if magnitude == 'billion':
                    result['labor_force_value_billion'] = value
                    result['labor_force_value'] = int(value * 1_000_000_000)
                elif magnitude == 'million':
                    result['labor_force_value'] = int(value * 1_000_000)

            year_match = re.search(r'\((\d{4})', text)
            if year_match:
                result['labor_force_year'] = int(year_match.group(1))

    # Parse "Agricultural products"
    agri_data = econ_data.get("Agricultural products", {})
    if agri_data:
        text = agri_data.get("text", "")
        if text:
            soup = BeautifulSoup(text, "html.parser")
            clean_text = soup.get_text()

            # Extract top products list
            products_match = re.search(r'top ten.*?by.*?tonnage[:\s]*(.+?)(?:\(\d{4}\)|$)', clean_text, re.IGNORECASE | re.DOTALL)
            if products_match:
                products_str = products_match.group(1)
                products = [p.strip() for p in products_str.split(',') if p.strip()]
                if products:
                    result['top_agricultural_products'] = products

            # Extract year
            year_match = re.search(r'\((\d{4})\)', clean_text)
            if year_match:
                result['agricultural_products_year'] = int(year_match.group(1))

    # Parse "Industrial production growth rate"
    industrial_data = econ_data.get("Industrial production growth rate", {})
    if industrial_data:
        text = industrial_data.get("text", "")
        if text:
            match = re.search(r'([\d.]+)%', text)
            if match:
                result['industrial_production_growth_rate'] = float(match.group(1))

            year_match = re.search(r'\((\d{4})', text)
            if year_match:
                result['industrial_production_year'] = int(year_match.group(1))

    # Parse "Exports - commodities"
    exports_comm = econ_data.get("Exports - commodities", {})
    if exports_comm:
        text = exports_comm.get("text", "")
        if text:
            soup = BeautifulSoup(text, "html.parser")
            clean_text = soup.get_text()
            commodities = [c.strip() for c in clean_text.split(',') if c.strip()]
            if commodities:
                result['top_export_commodities'] = commodities

    # Parse "Imports - commodities"
    imports_comm = econ_data.get("Imports - commodities", {})
    if imports_comm:
        text = imports_comm.get("text", "")
        if text:
            soup = BeautifulSoup(text, "html.parser")
            clean_text = soup.get_text()
            commodities = [c.strip() for c in clean_text.split(',') if c.strip()]
            if commodities:
                result['top_import_commodities'] = commodities

    # Parse "Taxes and other revenues"
    taxes_data = econ_data.get("Taxes and other revenues", {})
    if taxes_data:
        text = taxes_data.get("text", "")
        if text:
            match = re.search(r'([\d.]+)%\s*(?:of\s*GDP)?', text, re.IGNORECASE)
            if match:
                result['taxes_revenue_percent_gdp'] = float(match.group(1))

    return result


# Example usage
if __name__ == "__main__":
    import json
    import os

    json_path = os.path.join(os.path.dirname(__file__), '../../../../_raw_data/world/xx.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    econ_data = data.get("Economy", {})
    parsed = parse_economy_world(econ_data, "WLD")
    from pprint import pprint
    pprint(parsed)
