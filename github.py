import requests
import os
from dotenv import load_dotenv

# LOAD ENV
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

GITHUB_API_URL = "https://api.github.com/repos/Nerinyan/Nerinyan-i18n/contents"
GITHUB_HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {GITHUB_TOKEN}"
}

def fetch_file_list():
    response = requests.get(GITHUB_API_URL, headers=GITHUB_HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch file list: {response.status_code}")