"""
Driver script to dump app versions for all platforms.
"""

from google_play import scrape_zxbase_version
from apple_app_store import AppleAppStore


def main():
    """
    Driver script to get the latest version of the app from all stores.
    """
    print(f"{'Android':<10} {scrape_zxbase_version()}")

    apple_app = AppleAppStore("zxbase", "1608405737")
    print(f"{'iOS':<10} {apple_app.scrape_ios_version()}")
    print(f"{'iPad':<10} {apple_app.scrape_ipad_version()}")
    print(f"{'macOS':<10} {apple_app.scrape_macos_version()}")

    # TBD: Windows, Linux


if __name__ == "__main__":
    main()
