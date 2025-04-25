"""
Scrape public Google Play URL for the latest version of the app + driver script.
"""

import re
import requests
from bs4 import BeautifulSoup


def get_version(url: str):
    """
    Get the latest version of the app from the Google Play URL.
    """
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    scripts = soup.find_all("script")
    for script in scripts:
        match = re.search(r"[1-9]\d*\.\d+\.\d+", script.text)
        if match:
            return match[0]
    return None


def main():
    """
    Driver script to get the latest version of the app from the Google Play URL.
    """
    url = "https://play.google.com/store/apps/details?id=com.zxbase.base"
    version = get_version(url)
    print(version)


if __name__ == "__main__":
    main()
