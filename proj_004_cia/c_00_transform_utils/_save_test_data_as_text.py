import os
import json
from typing import List, Dict, Any


def save_test_data_as_text(test_data: List[Dict], test_folder: str, file_name: str) -> str:
    """
    Save test data to a formatted text file for inspection

    Args:
        test_data: List of dictionaries containing country data
        test_folder: Directory path where file will be saved
        file_name: Name of the file (will be converted to lowercase with .txt extension)

    Returns:
        str: Full path of the saved file

    Example:
        test_data = [
            {"USA": {"text": "50 states and 1 federal district", "note": "additional info"}},
            {"FRA": {"text": "18 regions", "note": "metropolitan and overseas"}}
        ]
        save_test_data_as_text(test_data, "C:/test_folder", "Administrative_Divisions")
    """

    # Ensure folder exists
    os.makedirs(test_folder, exist_ok=True)

    # Format filename
    formatted_filename = file_name.lower().replace(' ', '_') + '.txt'
    file_path = os.path.join(test_folder, formatted_filename)

    # Generate formatted content
    content_lines = []
    content_lines.append(f"{file_name.upper()} >> CIA Property Test Data")
    content_lines.append("=" * 50)
    content_lines.append("")

    for index, country_data in enumerate(test_data, 1):
        for iso3_code, data in country_data.items():
            content_lines.append(f"{index}. {iso3_code}")
            content_lines.append("-" * 30)

            # Format the data content
            if isinstance(data, dict):
                # Pretty format dictionary data
                formatted_data = json.dumps(data, indent=2, ensure_ascii=False)
                content_lines.append(f"Original Data: {formatted_data}")
            else:
                # Handle non-dict data
                content_lines.append(f"Original Data: {data}")

            content_lines.append("")  # Add blank line between entries

    # Write to file
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(content_lines))

        print(f"✅ Test data saved to: {file_path}")
        return file_path

    except Exception as e:
        print(f"❌ Error saving test data: {e}")
        raise


def save_test_data_with_results(test_data: List[Dict], test_folder: str, file_name: str,
                                parser_function, parser_name: str = "Parser") -> str:
    """
    Save test data along with parser results for comprehensive testing documentation

    Args:
        test_data: List of dictionaries containing country data
        test_folder: Directory path where file will be saved
        file_name: Name of the file (will be converted to lowercase with .txt extension)
        parser_function: Function to parse the test data
        parser_name: Name of the parser for display purposes

    Returns:
        str: Full path of the saved file
    """

    # Ensure folder exists
    os.makedirs(test_folder, exist_ok=True)

    # Format filename
    formatted_filename = f"{file_name.lower().replace(' ', '_')}_with_results.txt"
    file_path = os.path.join(test_folder, formatted_filename)

    # Generate formatted content
    content_lines = []
    content_lines.append(f"CIA Property Test Data - {parser_name}")
    content_lines.append("=" * 50)
    content_lines.append("")

    for index, country_data in enumerate(test_data, 1):
        for iso3_code, data in country_data.items():
            content_lines.append(f"{index}. {iso3_code}")
            content_lines.append("-" * 30)

            # Original data
            if isinstance(data, dict):
                formatted_data = json.dumps(data, indent=2, ensure_ascii=False)
                content_lines.append(f"Original Data: {formatted_data}")
            else:
                content_lines.append(f"Original Data: {data}")

            content_lines.append("")

            # Parser results
            try:
                result = parser_function(test_data=data, iso3Code=iso3_code)
                formatted_result = json.dumps(
                    result, indent=2, ensure_ascii=False)
                content_lines.append(f"Parsed Result:")
                content_lines.append(formatted_result)

                # Structure validation
                if isinstance(result, dict):
                    content_lines.append("✅ Structure validation passed")
                else:
                    content_lines.append(
                        "❌ Structure validation failed - not a dict")

            except Exception as e:
                content_lines.append(f"❌ Parser Error: {e}")

            content_lines.append("")
            content_lines.append("=" * 50)
            content_lines.append("")

    # Write to file
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(content_lines))

        print(f"✅ Test data with results saved to: {file_path}")
        return file_path

    except Exception as e:
        print(f"❌ Error saving test data with results: {e}")
        raise


# Example usage function for testing
def example_usage():
    """Example of how to use the save_test_data_as_text function"""

    # Sample test data (matching your format)
    sample_test_data = [
        {"USA": {
            "text": "50 states and 1 federal district; 12 statistical areas*",
            "note": "*the 12 statistical areas include 11 statistical divisions and 1 statistical region"
        }},
        {"FRA": {
            "text": "18 regions (regions, singular - region); note - France is divided into 13 metropolitan regions (including the \"collectivity\" of Corsica) and 5 overseas regions",
            "note": "additional administrative divisions"
        }},
        {"DEU": {
            "text": "16 states (Laender, singular - Land); Baden-Wuerttemberg, Bayern (Bavaria), Berlin, Brandenburg, Bremen, Hamburg, Hessen (Hesse), Mecklenburg-Vorpommern (Mecklenburg-West Pomerania), Niedersachsen (Lower Saxony), Nordrhein-Westfalen (North Rhine-Westphalia), Rheinland-Pfalz (Rhineland-Palatinate), Saarland, Sachsen (Saxony), Sachsen-Anhalt (Saxony-Anhalt), Schleswig-Holstein, Thueringen (Thuringia)"
        }}
    ]

    # Test folder path
    test_folder = r"C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\c_05_government\helper\_test_files"

    # Save test data
    saved_file = save_test_data_as_text(
        test_data=sample_test_data,
        test_folder=test_folder,
        file_name="Administrative_Divisions"
    )

    print(f"File saved at: {saved_file}")


if __name__ == "__main__":
    example_usage()
