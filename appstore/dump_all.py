"""
Driver script to dump app versions for all platforms.
"""

from scrape_version import scrape_snapcraft_version
from scrape_version import scrape_google_play_version
from apple_app_store import AppleAppStore


def main():
    """
    Driver script to get the latest version of the app from all stores.
    """
    print(f"{'Android':<10} {scrape_google_play_version()}")

    apple_app = AppleAppStore("zxbase", "1608405737")
    print(f"{'iOS':<10} {apple_app.scrape_ios_version()}")
    print(f"{'iPad':<10} {apple_app.scrape_ipad_version()}")
    print(f"{'macOS':<10} {apple_app.scrape_macos_version()}")
    print(f"{'Linux':<10} {scrape_snapcraft_version()}")

    # TBD: Windows


if __name__ == "__main__":
    main()
