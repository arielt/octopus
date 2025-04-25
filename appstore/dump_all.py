"""
Driver script to dump app versions for all platforms.
"""

from dataclasses import dataclass


@dataclass
class AppStoreApp:
    """
    Represents an app in the App Store.
    """
    platform: str
    store: str
    app_id: str
    version: str = "Undetected"


apps = [
    AppStoreApp(platform="Android", store="Google Play", app_id="com.example.app"),
    AppStoreApp(platform="iOS", store="MacApp Store", app_id="com.example.app"),
    AppStoreApp(platform="macOS", store="MacApp Store", app_id="com.example.app"),
    AppStoreApp(platform="iPad", store="MacApp Store", app_id="com.example.app"),
    AppStoreApp(platform="Windows", store="Microsoft Store", app_id="com.example.app"),
    AppStoreApp(platform="Linux", store="Snapcraft", app_id="com.example.app"),
]

for app in apps:
    print(f"{app.platform:<10} {app.version:<10}")
