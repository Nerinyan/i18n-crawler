import requests
import os

def download_json_files(file_list, session, download_dir):
    for file in file_list:
        if file['name'].endswith('.json'):
            file_path = os.path.join(download_dir, file['name'])
            response = requests.get(file['download_url'])
            if response.status_code == 200:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"Downloaded {file['name']} successfully.")
            else:
                print(f"Failed to download {file['name']}: {response.status_code}")
                print(f"URL: {file['download_url']}")
