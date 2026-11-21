import requests
import zipfile
from datetime import datetime
from dotenv import load_dotenv
import os

from config.paths import SUPERSET_EXPORT_DIR, SUPERSET_ENV_FILE_PATH

# Load environment variables
load_dotenv(SUPERSET_ENV_FILE_PATH)

SUPERSET_URL = os.getenv("SUPERSET_URL")
SUPERSET_USERNAME = os.getenv("SUPERSET_USERNAME")
SUPERSET_PASSWORD = os.getenv("SUPERSET_PASSWORD")

SUPERSET_EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def authenticate():
    response = requests.post(
        f"{SUPERSET_URL}/api/v1/security/login",
        json={
            "username": SUPERSET_USERNAME,
            "password": SUPERSET_PASSWORD,
            "provider": "db",
            "refresh": True
        },
        timeout=30
    )
    response.raise_for_status()

    return response.json()["access_token"]


def export_assets(token):
    response = requests.get(
        f"{SUPERSET_URL}/api/v1/assets/export/",
        headers={"Authorization": f"Bearer {token}"},
        timeout=120
    )
    response.raise_for_status()

    filename = (
        f"superset_assets_{datetime.now():%Y%m%d_%H%M%S}.zip"
    )

    file_path = SUPERSET_EXPORT_DIR / filename
    file_path.write_bytes(response.content)

    # Verify ZIP integrity
    with zipfile.ZipFile(file_path, "r") as archive:
        if archive.testzip() is not None:
            raise ValueError("Corrupted ZIP archive.")

    print(f"Export successful: {file_path}")
    size_mb = file_path.stat().st_size / (1024 ** 2)
    print(f"File size: {size_mb:.2f} Mo")


def main():
    try:
        token = authenticate()
        export_assets(token)

    except requests.RequestException as error:
        print(f"Superset API error: {error}")

    except Exception as error:
        print(f"Export failed: {error}")


if __name__ == "__main__":
    main()