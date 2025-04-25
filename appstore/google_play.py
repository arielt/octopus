"""
Scrape public Google Play URL for the latest version of the app + driver script.
"""

import re
import requests
from bs4 import BeautifulSoup


def scrape_google_play_version(url: str):
    """
    Scrape the latest version of the app from the Google Play URL.
    """
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    scripts = soup.find_all("script")
    for script in scripts:
        match = re.search(r"[1-9]\d*\.\d+\.\d+", script.text)
        if match:
            return match[0]
    return None


def scrape_zxbase_version():
    """
    Scrape the latest version of Zxbase from the Google Play URL.
    """
    return scrape_google_play_version(
        "https://play.google.com/store/apps/details?id=com.zxbase.base"
    )


def main():
    """
    Driver script to get the latest version of the app from the Google Play URL.
    """
    print(f"{'Android':<10} {scrape_zxbase_version()}")


if __name__ == "__main__":
    main()
