from bs4 import BeautifulSoup

import requests

from common.utils import Extension
from common.utils.utility import download_file

DOWNLOAD_BASE_URL = "https://www.elitigation.sg/gd/gd/"


def extract_and_download(query, current_page=1):
    SEARCH_URL = "https://www.elitigation.sg/gd/Home/Index?filter=SUPCT&yearOfDecision=All&sortBy=Score&currentPage=" + str(
        current_page) + "&sortAscending=False&searchPhrase=" + query + "&verbose=False"
    payload = requests.get(SEARCH_URL, allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})
    soup = BeautifulSoup(payload.content, "html.parser")
    full_links_list = set(soup.find_all("a", href=True))

    document_links = [doc for doc in full_links_list if doc['href'].startswith("/gd/s/")]
    doc_id_links = []
    for doc in document_links:
        doc_id = doc['href'].split('/')[3]
        doc_id_links.append(doc_id)

    for link in doc_id_links:
        response, save_path = download_file(base_url=DOWNLOAD_BASE_URL, link=link,
                                            extension=Extension.Extension.SlashPDF.value)
        if response.status_code != 200:
            response, save_path = download_file(base_url=DOWNLOAD_BASE_URL, link=link, extension=Extension.RTF.value)
            if response.status_code != 200:
                response, save_path = download_file(base_url=DOWNLOAD_BASE_URL, link=link,
                                                    extension=Extension.HTML.value)
                if response.status_code != 200:
                    print("cannot find the pdf, rtf or html document for document link : " + link)
        if response.status_code == 200:
            print(save_path)
            with open(save_path, 'wb') as f:
                f.write(response.content)
    return payload


def run():
    query_list = [
        "\"insolvency\" AND \"ethics\"",
        "\"insolvency\" AND \"ethical behavior\"",
        "\"insolvency\" AND \"code of ethics\"",
        "\"insolvency\" AND \"practitioner\"",
        "\"insolvency\" AND \"liquidator\"",
        "\"insolvency\" AND \"misconduct\"",
        "\"insolvency\" AND \"Lack of impartiality\"",
        "\"insolvency\" AND \"Breach of duty of care\"",
        "\"insolvency\" AND \"Standards of conduct\"",
        "\"insolvency\" AND \"Code of conduct\""
    ]

    for query in query_list:

        # SEARCH_URL = "https://www.elitigation.sg/gd/Home/Index?filter=SUPCT&yearOfDecision=All&sortBy=Score&currentPage=1&sortAscending=False&searchPhrase=%22insolvency%22%20AND%20%22liquidator%22&verbose=False"
        SEARCH_URL = "https://www.elitigation.sg/gd/Home/Index?filter=SUPCT&yearOfDecision=All&sortBy=Score&currentPage=1&sortAscending=False&searchPhrase=" + query + "&verbose=False"
        payload = requests.get(SEARCH_URL, allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})

        soup = BeautifulSoup(payload.content, "html.parser")
        full_links_list = set(soup.find_all("a", href=True))

        document_links = [doc for doc in full_links_list if doc['href'].startswith("/gd/s/")]
        pagination_links = [page for page in full_links_list if
                            page['href'].startswith("/gd/Home/Index?Filter=")]
        doc_id_links = []

        # print(document_links)
        # print(pagination_links)
        page_numbers = []
        for page in pagination_links:
            contents = page.contents
            for content in contents:
                if not str(content).startswith('<') and content.isdigit():
                    page_numbers.append(int(content))

        for num in page_numbers:
            extract_and_download(query, num)


if __name__ == '__main__':
    run()
