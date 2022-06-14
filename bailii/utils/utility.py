import os

import requests

BASE_URL = "https://www.bailii.org"


def download_file(link, extension='.html'):
    response = requests.get(BASE_URL + link + extension, allow_redirects=True,
                            headers={"User-Agent": "Chrome/102.0.0.0"})  # mimic the browser
    save_path = os.path.join(".", "downloads", str(link).replace('/', '_') + extension)
    return response, save_path


def is_valid_size(file):
    return os.path.getsize(file) / 1024 < 20  # check if the document is less than 20kb
