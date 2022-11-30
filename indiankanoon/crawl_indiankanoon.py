import os

from bs4 import BeautifulSoup

import requests

from common.utils import Extension
from common.utils.utility import download_file

COOKIE = "_ga=GA1.2.607408111.1660651683; _gid=GA1.2.24101006.1660651683; sessionid=o1eeywcjnl2w0oto9ixnhhrqi7h29zf5; cf_chl_2=b05057d6594e8e2; cf_chl_prog=x25; cf_clearance=DArjglwTE5biGmT244qH3aepz.xR.QbFHQdY0_jbRkc-1660739215-0-150; __cf_bm=mMw4vCn7L1eCp5xyomulo3k0z6pE2Fh8_0IbHftZs4M-1660739217-0-AftYgdRP/g4XCDJoVGWdBh/bAyB9G3mJReVR5Y3DmflFH7GOczrqFF6welWOZazSTymbEBRdnMYCPLBemnXs36XpbpIf3bxeFMvQjc0+DE6OkJoEFiWxa3iBPyPa0r+VIA==; _gat=1"


def extract_and_download(query, pagenum=1):
    SEARCH_URL = "https://indiankanoon.org/search/?formInput=" + query + "+doctypes:+judgments&pagenum=" + str(pagenum)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "cookie": COOKIE,
        "content-type": "application/pdf"
    }
    payload = requests.get(SEARCH_URL, allow_redirects=True, headers=headers)
    soup = BeautifulSoup(payload.content, "html.parser")
    full_links_list = set(soup.find_all("a", href=True))

    document_links = [doc for doc in full_links_list if doc['href'].__contains__("/docfragment/")]
    for doc in document_links:
        doc_id = doc['href'].split('/')[2]
        params = {
            "action": "/doc/" + doc_id + "/"
        }
        url = "https://indiankanoon.org/doc/" + doc_id + "/"
        response = requests.post(url, allow_redirects=True, headers=headers, data=params,params=params)
        save_path = os.path.join("", "downloads", str(doc_id).replace('/', '_') + Extension.Extension.PDF.value)
        if response.status_code == 200:
            print(save_path)
            with open(save_path, 'wb') as f:
                f.write(response.content)
        # loaded_doc = set(doc_soup.find_all("a", href=True))
        #
        # for lnk in loaded_doc:
        #     if lnk.contents[0].__contains__("Original Word Document"):
        #         split = lnk['href'].split('/')
        #         link = split[len(split) - 1]
        #         version = link.split('v=')[1]
        #         doc_link = link.split('v=')[0].split('.')[0]
        #         extention = '.' + link.split('v=')[0].split('.')[1].replace('?', '')
        #         base_url = '/'.join(split[0:len(split) - 1]) + '/'
        #         response, save_path = download_file(base_url=base_url, link=doc_link, extension=extention,
        #                                             version=version)
        #

    return payload


def run():
    query_list = [
        "insolvency+ethics",
        "insolvency+ethical+behavior",
        "insolvency+code+of+ethics",
        "insolvency+practitioner",
        "insolvency+liquidator",
        "insolvency+misconduct",
        "insolvency+Lack+of+impartiality",
        "insolvency+Breach+of+duty+of+care",
        "insolvency+Standards+of+conduct",
        "insolvency+Code+of+conduct"
    ]

    for query in query_list:

        SEARCH_URL = "https://indiankanoon.org/search/?formInput=" + query + "+doctypes:+judgments"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "cookie": COOKIE,
        }
        payload = requests.get(SEARCH_URL, allow_redirects=True, headers=headers)

        soup = BeautifulSoup(payload.content, "html.parser")
        full_links_list = set(soup.find_all("a", href=True))

        document_links = [doc for doc in full_links_list if doc['href'].__contains__("/docfragment/")]
        pagination_links = [page for page in full_links_list if
                            page['href'].__contains__("pagenum=")]

        page_numbers = [1]
        for page in pagination_links:
            content = page.contents
            arr = page.attrs['href'].split('&')
            for split in arr:
                for cont in content:
                    if split.startswith('pagenum') and cont.isdigit():
                        page_numbers.append(cont)

        for num in page_numbers:
            extract_and_download(query, num)


if __name__ == '__main__':
    run()
