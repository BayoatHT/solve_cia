"""
Parse visual attributes: main image and image gallery.
"""

from typing import Dict, List
from proj_004_cia.___proj_heritage.__utils.handle_null_values import handle_missing_image


def parse_visual(site: Dict) -> Dict:
    """
    Parse all visual attributes from raw site data.

    Args:
        site: Raw site dictionary

    Returns:
        Dictionary with main image and gallery data

    Example:
        >>> site = {
        ...     "main_image_url": {
        ...         "url": "https://...",
        ...         "filename": "site_570_0001.jpg",
        ...         "width": 1840,
        ...         "height": 1232
        ...     },
        ...     "images_urls": "https://img1.jpg, https://img2.jpg"
        ... }
        >>> parse_visual(site)
        {
            'main_image': {...},
            'gallery': {...}
        }
    """
    # Parse main image
    main_image = handle_missing_image(
        main_image=site.get('main_image_url'),
        gallery_urls=site.get('images_urls')
    )

    # Parse gallery
    gallery_urls = parse_image_gallery(site.get('images_urls', ''))

    return {
        'main_image': main_image,
        'gallery': {
            'urls': gallery_urls,
            'count': len(gallery_urls)
        }
    }


def parse_image_gallery(images_urls_str: str) -> List[str]:
    """
    Parse comma-separated image URLs into list.

    Args:
        images_urls_str: Comma-separated URLs

    Returns:
        List of URL strings

    Example:
        >>> parse_image_gallery("https://img1.jpg, https://img2.jpg")
        ['https://img1.jpg', 'https://img2.jpg']
    """
    if not images_urls_str:
        return []

    # Split and clean URLs
    urls = [url.strip() for url in images_urls_str.split(',')]

    # Filter out empty strings
    urls = [url for url in urls if url]

    return urls
