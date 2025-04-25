"""
Scrape version looking string from URL.
"""

import re
import requests
from bs4 import BeautifulSoup

SNAPCRAFT_URL = "https://snapcraft.io/zxbase"
GOOGLE_PLAY_URL = "https://play.google.com/store/apps/details?id=com.zxbase.base"


def scrape_version(url: str):
    """
    Scrape the first match of x.y.z entry in scripts, where x is not zero
    """
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    scripts = soup.find_all("script")
    for script in scripts:
        match = re.search(r"[1-9]\d*\.\d+\.\d+", script.text)
        if match:
            return match[0]
    return None


def scrape_snapcraft_version():
    """
    Scrape the latest version of the app from the Google Play URL.
    """
    return scrape_version(SNAPCRAFT_URL)


def scrape_google_play_version():
    """
    Scrape the latest version of the app from the Google Play URL.
    """
    return scrape_version(GOOGLE_PLAY_URL)


def main():
    """
    Driver script.
    """
    print(f"{'Android':<10} {scrape_google_play_version()}")
    print(f"{'Linux':<10} {scrape_snapcraft_version()}")


if __name__ == "__main__":
    main()
