import re
import logging

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_wonders_of_the_world(wonders_data: dict, iso3Code: str = None) -> dict:
    """
    Parses the 'Wonders of the World' data.

    Parameters:
        wonders_data (dict): The 'Wonders of the World' section from the data.

    Returns:
        dict: A dictionary containing parsed details of the wonders, categorized by type.
    """
    result = {}

    for category, data in wonders_data.items():
        # Initialize category in result dictionary
        result[category] = {
            "description": "",
            "wonders": [],
            "note": ""
        }

        # Extract the text content
        text = data.get("text", "")
        if text:
            # Split text by paragraphs
            paragraphs = re.split(r'</?p>', text)
            wonders_list = []
            for paragraph in paragraphs:
                paragraph = paragraph.strip()
                if not paragraph:
                    continue
                # Extract numbered wonders or description
                if re.match(r'^\d+\.\s*<strong>.*?</strong>', paragraph):
                    # This is a wonder entry
                    match = re.match(
                        r'^\d+\.\s*<strong>(.*?)</strong><br>(.*)', paragraph)
                    if match:
                        name = match.group(1).strip()
                        # Remove any HTML tags
                        details = re.sub(r'<.*?>', '', match.group(2)).strip()
                        wonders_list.append({
                            "name": name,
                            "details": details
                        })
                elif paragraph.startswith("note:"):
                    # This is a note
                    # Remove any HTML tags
                    note_text = re.sub(r'<.*?>', '', paragraph).strip()
                    result[category]["note"] = note_text
                else:
                    # This is a general description
                    description_text = re.sub(
                        r'<.*?>', '', paragraph).strip()  # Remove any HTML tags
                    result[category]["description"] = description_text

            # Assign wonders list to the category
            result[category]["wonders"] = wonders_list

    return result


# Example usage
if __name__ == "__main__":
    wonders_data = {
        "The Seven Wonders of the Ancient World": {
            # Truncated for brevity
            "text": "<p>The conquests of Alexander the Great (r. 336-323 B.C.) in the fourth century B.C. fostered the spread of Greek culture..."
        },
        "The New Seven Wonders of the World": {
            "text": "<p>A private initiative to come up with a new list for seven of the world’s wonders sprang up early in the new Millennium..."  # Truncated for brevity
        }
    }
    parsed_data = parse_wonders_of_the_world(wonders_data)
    print(parsed_data)
