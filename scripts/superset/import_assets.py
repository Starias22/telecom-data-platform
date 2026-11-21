import os
import zipfile
import requests

from dotenv import load_dotenv

from config.paths import SUPERSET_EXPORT_DIR, SUPERSET_ENV_FILE_PATH



# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv(SUPERSET_ENV_FILE_PATH)

SUPERSET_URL = os.getenv(
    "SUPERSET_URL",
    "http://localhost:8088"
).rstrip("/")

SUPERSET_USERNAME = os.getenv("SUPERSET_USERNAME")
SUPERSET_PASSWORD = os.getenv("SUPERSET_PASSWORD")


# ============================================================
# VALIDATION
# ============================================================

if not SUPERSET_USERNAME or not SUPERSET_PASSWORD:
    raise ValueError(
        "SUPERSET_USERNAME or SUPERSET_PASSWORD missing in .env"
    )

if not SUPERSET_EXPORT_DIR.exists():
    raise FileNotFoundError(
        f"Export directory not found: {SUPERSET_EXPORT_DIR}"
    )

archives = sorted(
    SUPERSET_EXPORT_DIR.glob("superset_assets_*.zip"),
    key=lambda path: path.stat().st_mtime,
    reverse=True
)

if not archives:
    raise FileNotFoundError(
        "No Superset export archive found."
    )

zip_path = archives[0]

print(f"\nSelected archive: {zip_path.name}")


# ============================================================
# VERIFY ARCHIVE
# ============================================================

print("\nChecking archive integrity...")

with zipfile.ZipFile(zip_path, "r") as archive:
    corrupted_file = archive.testzip()

    if corrupted_file:
        raise RuntimeError(
            f"Corrupted file in archive: {corrupted_file}"
        )

    print("Archive integrity verified.")

    dashboard_files = [
        name for name in archive.namelist()
        if "/dashboards/" in name and name.endswith(".yaml")
    ]

    print(f"Dashboards found: {len(dashboard_files)}")


# ============================================================
# CREATE SESSION
# ============================================================

session = requests.Session()


# ============================================================
# AUTHENTICATION
# ============================================================

print("\nAuthenticating with Superset...")

login_response = session.post(
    f"{SUPERSET_URL}/api/v1/security/login",
    json={
        "username": SUPERSET_USERNAME,
        "password": SUPERSET_PASSWORD,
        "provider": "db",
        "refresh": True
    },
    headers={
        "Accept": "application/json"
    },
    timeout=30
)

login_response.raise_for_status()

access_token = login_response.json().get("access_token")

if not access_token:
    raise RuntimeError(
        "Authentication failed: access token not returned."
    )

headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/json"
}

print("Authentication successful.")


# ============================================================
# VERIFY AUTHENTICATION
# ============================================================

print("\nVerifying authenticated user...")

me_response = session.get(
    f"{SUPERSET_URL}/api/v1/me/",
    headers=headers,
    timeout=30
)

me_response.raise_for_status()

print("Authenticated user verified.")


# ============================================================
# GET CSRF TOKEN
# ============================================================

print("\nRetrieving CSRF token...")

csrf_response = session.get(
    f"{SUPERSET_URL}/api/v1/security/csrf_token/",
    headers=headers,
    timeout=30
)

csrf_response.raise_for_status()

csrf_token = csrf_response.json().get("result")

if not csrf_token:
    raise RuntimeError(
        "Could not retrieve CSRF token."
    )

headers["X-CSRFToken"] = csrf_token
headers["Referer"] = SUPERSET_URL

print("CSRF token retrieved.")

# ============================================================
# IMPORT OPTIONS
# ============================================================

print("\nImport options:")
print("  1. Safe import (default): Do not overwrite existing assets.")
print("  2. Overwrite: Replace existing assets with those in the archive.")

overwrite = False

choice = input("\nSelect import mode (1/2): ").strip()

if choice == "1":
    print("This is the latest version of Superset (version 6.1.0), and it does not support safe import correctly. Import Cancelled.")
    exit()
if choice == "2":
    print(
        "\nWARNING: This operation will overwrite existing "
        "dashboards, charts, datasets and databases."
    )

    confirmation = input(
        "Type OVERWRITE to confirm: "
    ).strip()

    if confirmation == "OVERWRITE":
        overwrite = True
    else:
        print("\nConfirmation failed. Import cancelled.")
        exit()

elif choice != "1":
    print("\nInvalid choice. Import cancelled.")
    exit()

# ============================================================
# IMPORT ASSETS
# ============================================================

print(f"\nImporting: {zip_path.name}")

with open(zip_path, "rb") as archive:

    response = session.post(
        f"{SUPERSET_URL}/api/v1/assets/import/",
        headers=headers,
        files={
            "bundle": (
                zip_path.name,
                archive,
                "application/zip"
            )
        },
        data={
            "overwrite": str(overwrite)
        },
        allow_redirects=False,
        timeout=300
    )


# ============================================================
# HANDLE RESPONSE
# ============================================================

print("\nImport response:")
print("HTTP status:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))

if response.status_code not in (200, 201):
    print("Response body:")
    print(response.text[:3000])

response.raise_for_status()

if "application/json" in response.headers.get(
    "Content-Type", ""
):
    result = response.json()
    print("Server response:", result)

    if result.get("message") == "OK":
        print("\nImport completed successfully!")
    else:
        print("\nImport request completed. Check server response.")
else:
    print("\nUnexpected response format:")
    print(response.text[:2000])
    raise RuntimeError(
        "Import response was not JSON. Import success cannot be confirmed."
    )