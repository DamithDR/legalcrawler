from bs4 import BeautifulSoup

import requests

from bailii.utils.Extension import Extension
from bailii.utils.utility import download_file

print("crawling job started...")

# only UK cases considered at the moment
SEARCH_URL = "https://www.bailii.org/cgi-bin/lucy_search_1.cgi?method=boolean&query=(insolvency) AND (ethics)&mask_path=/uk/cases&datehigh=&highlight=1&sort=rank&start=0&show=1000"

payload = requests.get(SEARCH_URL, allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})

soup = BeautifulSoup(payload.content, "html.parser")
full_links_list = set(soup.find_all("a", href=True))

document_links = [doc for doc in full_links_list if doc['href'].startswith("/cgi-bin/format.cgi?doc=")]
doc_id_links = []

for doc in document_links:
    doc_id = doc['href'].split('&')[0].split('doc=')[1].split('.')[0]
    doc_id_links.append(doc_id)

for link in doc_id_links:
    response, save_path = download_file(link, Extension.PDF.value)
    if response.status_code != 200:
        response, save_path = download_file(link, Extension.RTF.value)
        if response.status_code != 200:
            response, save_path = download_file(link, Extension.HTML.value)
            if response.status_code != 200:
                print("cannot find the pdf, rtf or html document for document link : " + link)
    if response.status_code == 200:
        print(save_path)
        with open(save_path, 'wb') as f:
            f.write(response.content)

# will consider seperating the documents later
# eng_wales, scotland, ie, nie = [doc for doc in a_links_list if
#                               doc['href'].startswith("/cgi-bin/format.cgi?doc=/ew/cases")], \
#                              [doc for doc in a_links_list if
#                               doc['href'].startswith("/cgi-bin/format.cgi?doc=/scot/cases")], \
#                              [doc for doc in a_links_list if
#                               not doc['href'].startswith("/cgi-bin/format.cgi?doc=/ie/cases")], \
#                              [doc for doc in a_links_list if
#                               not doc['href'].startswith("/cgi-bin/format.cgi?doc=/nie/cases")]


print("crawling job end, crawled : " + str(len(doc_id_links)) + " documents")
