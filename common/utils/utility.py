import os

import requests


def download_file(base_url, link, extension='.html', version=None):
    if version is None:
        vers = ''
    else:
        vers = '?v=' + version
    response = requests.get(base_url + link + extension + vers, allow_redirects=True,
                            headers={"User-Agent": "Chrome/102.0.0.0"})  # mimic the browser
    if extension == '/pdf':
        extension = '.pdf'
    save_path = os.path.join("", "downloads", str(link).replace('/', '_') + extension)
    return response, save_path


def is_valid_size(file):
    return os.path.getsize(file) / 1024 < 20  # check if the document is less than 20kb
