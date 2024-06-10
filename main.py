import time
import threading
from flask import Flask, jsonify, send_from_directory
from datetime import datetime, timezone
from github import fetch_file_list
from db import init_db, get_session, upsert_files, get_file_list
from download import download_json_files

# DATABASE Initialize
init_db()
session = get_session()

# SETUP DOWNLOAD ROOT
DOWNLOAD_DIR = 'downloads'

# THREAD COOLDOWN
THREAD_DELAY = 1800

last_run_time = None  

def check_and_update_files():
    global last_run_time
    file_list = fetch_file_list()
    upsert_files(file_list, session)
    download_json_files(file_list, session, DOWNLOAD_DIR)
    last_run_time = datetime.now(timezone.utc)

def worker():
    while True:
        check_and_update_files()
        time.sleep(THREAD_DELAY)

thread = threading.Thread(target=worker)
thread.daemon = True
thread.start()

app = Flask(__name__)

@app.route('/lang/list', methods=['GET'])
def get_lang_list():
    file_list = get_file_list(session)
    langs = sorted(set(f.split('/')[0] for f in file_list))
    return jsonify([{'list': langs}, {'last_run_time': last_run_time.isoformat() if last_run_time else "Never"}])

@app.route('/lang/<lang>', methods=['GET'])
def get_lang_file(lang):
    filename = f"{lang}.json"
    return send_from_directory(DOWNLOAD_DIR, filename)

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({"last_run_time": last_run_time.isoformat() if last_run_time else "Never"})

if __name__ == '__main__':
    app.run(debug=True)
