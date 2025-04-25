import requests
from bs4 import BeautifulSoup
import re

URL = "https://snapcraft.io/zxbase"

def scrape_snapcraft_version():
    """
    Scrape the latest version of the app from the Google Play URL.
    """
    response = requests.get(URL, timeout=10)
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
    print(f"{'Linux':<10} {scrape_snapcraft_version()}")


if __name__ == "__main__":
    main()
