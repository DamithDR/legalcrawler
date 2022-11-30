from bs4 import BeautifulSoup

import requests

from common.utils.Extension import Extension
from common.utils.utility import download_file

print("crawling job started...")
DOWNLOAD_BASE_URL = "https://www.bailii.org"

query_list = [
    "(insolvency) AND (ethics)",
    "(insolvency) AND (ethical behavior)",
    "(insolvency) AND (code of ethics)",
    "(insolvency) AND (practitioner)",
    "(insolvency) AND (liquidator)",
    "(insolvency) AND (misconduct)",
    "(insolvency) AND (Lack of impartiality)",
    "(insolvency) AND (Breach of duty of care)",
    "(insolvency) AND (Standards of conduct)",
    "(insolvency) AND (Code of conduct)"
]

for query in query_list:
    # only UK cases-temp considered at the moment
    SEARCH_URL = "https://www.bailii.org/cgi-bin/lucy_search_1.cgi?method=boolean&query=" + query + "&mask_path=/uk/cases-temp&datehigh=&highlight=1&sort=rank&start=0&show=1000"

    payload = requests.get(SEARCH_URL, allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})

    soup = BeautifulSoup(payload.content, "html.parser")
    full_links_list = set(soup.find_all("a", href=True))

    document_links = [doc for doc in full_links_list if doc['href'].startswith("/cgi-bin/format.cgi?doc=")]
    doc_id_links = []

    for doc in document_links:
        doc_id = doc['href'].split('&')[0].split('doc=')[1].split('.')[0]
        doc_id_links.append(doc_id)

    for link in doc_id_links:
        response, save_path = download_file(base_url=DOWNLOAD_BASE_URL, link=link, extension=Extension.PDF.value)
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

    # will consider seperating the documents later
    # eng_wales, scotland, ie, nie = [doc for doc in a_links_list if
    #                               doc['href'].startswith("/cgi-bin/format.cgi?doc=/ew/cases-temp")], \
    #                              [doc for doc in a_links_list if
    #                               doc['href'].startswith("/cgi-bin/format.cgi?doc=/scot/cases-temp")], \
    #                              [doc for doc in a_links_list if
    #                               not doc['href'].startswith("/cgi-bin/format.cgi?doc=/ie/cases-temp")], \
    #                              [doc for doc in a_links_list if
    #                               not doc['href'].startswith("/cgi-bin/format.cgi?doc=/nie/cases-temp")]

    print("crawling job end, crawled : " + str(len(doc_id_links)) + " documents")
