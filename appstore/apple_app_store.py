"""
Scrape public Apple App Store URL for the latest version of the app.
"""

import requests
from bs4 import BeautifulSoup


class AppleAppStore:
    def __init__(self, app_name: str, app_id: str):
        self.app_name = app_name
        self.app_id = app_id

    def version(self, platform: str):
        url = f"https://apps.apple.com/us/app/{self.app_name}/id{self.app_id}?platform={platform}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        version = soup.find("p", class_="whats-new__latest__version").text.strip()
        return version


def main():
    app = AppleAppStore("zxbase", "1608405737")
    print(f"{'iOS':<10} {app.version('ios')}")
    print(f"{'iPad':<10} {app.version('ipad')}")
    print(f"{'macOS':<10} {app.version('macos')}")


if __name__ == "__main__":
    main()
