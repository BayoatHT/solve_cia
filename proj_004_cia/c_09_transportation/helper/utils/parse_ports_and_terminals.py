"""
Parse ports and terminals data from CIA World Factbook (legacy field).
"""
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_ports_and_terminals(ports_and_terminals_data: dict, iso3Code: str = None) -> dict:
    """
    Parse ports and terminals data (legacy field, only 1 country).

    Args:
        ports_and_terminals_data: Dict with subfields like 'major seaport(s)'
        iso3Code: Country ISO3 code

    Returns:
        Dict with:
            - major_seaports: list of seaport names

    Example:
        Input: {"major seaport(s)": {"text": "Ad Dakhla, Laayoune (El Aaiun)"}}
        Output: {'major_seaports': ['Ad Dakhla', 'Laayoune (El Aaiun)']}
    """
    result = {}

    if not ports_and_terminals_data:
        return result

    try:
        if 'major seaport(s)' in ports_and_terminals_data:
            seaports_data = ports_and_terminals_data['major seaport(s)']
            if isinstance(seaports_data, dict) and 'text' in seaports_data:
                text = seaports_data['text']
                # Split by comma and clean
                seaports = [clean_text(p.strip()) for p in text.split(',') if p.strip()]
                if seaports:
                    result['major_seaports'] = seaports

    except Exception as e:
        logging.error(f"Error parsing ports_and_terminals for {iso3Code}: {e}")

    return result


# Example usage
if __name__ == "__main__":
    test_data = {
        "major seaport(s)": {"text": "Ad Dakhla, Laayoune (El Aaiun)"}
    }
    parsed = parse_ports_and_terminals(test_data)
    print(parsed)
