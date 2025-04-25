"""
Scrape public Apple App Store URL for the latest version of the app + driver script.
"""

import requests
from bs4 import BeautifulSoup


class AppleAppStore:
    """
    Scrape public Apple App Store URL for the latest version of the app.
    """

    def __init__(self, app_name: str, app_id: str):
        self.app_name = app_name
        self.app_id = app_id

    def scrape_version(self, platform: str):
        """
        Get the latest version of the app for a given platform.
        """
        url = f"https://apps.apple.com/us/app/{self.app_name}/id{self.app_id}?platform={platform}"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        version = soup.find("p", class_="whats-new__latest__version").text.strip()
        return version.split(" ")[-1]

    def scrape_ios_version(self):
        """
        Get the latest version of the app for iOS.
        """
        return self.scrape_version("ios")

    def scrape_ipad_version(self):
        """
        Get the latest version of the app for iPad.
        """
        return self.scrape_version("ipad")

    def scrape_macos_version(self):
        """
        Get the latest version of the app for macOS.
        """
        return self.scrape_version("macos")


def main():
    """
    Driver script to get the latest version of the app for all platforms.
    """
    app = AppleAppStore("zxbase", "1608405737")
    print(f"{'iOS':<10} {app.scrape_ios_version()}")
    print(f"{'iPad':<10} {app.scrape_ipad_version()}")
    print(f"{'macOS':<10} {app.scrape_macos_version()}")


if __name__ == "__main__":
    main()
