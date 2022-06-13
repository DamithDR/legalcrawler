import os.path

from bs4 import BeautifulSoup

import requests

BASE_URL = "https://www.bailii.org"
# webbrowser.open(BASE_URL)
#
# response = wget.download("https://www.bailii.org/ew/cases/EWHC/Admin/2012/2254.rtf", "doc.rtf")

# only UK cases considered at the moment
SEARCH_URL = "https://www.bailii.org/cgi-bin/lucy_search_1.cgi?method=boolean&query=(insolvency) AND (ethics)&mask_path=/uk/cases&datehigh=&highlight=1&sort=rank&highlight=1&&start=0&show=1000"

payload = requests.get(SEARCH_URL, allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})

print(payload.status_code)
soup = BeautifulSoup(payload.content, "html.parser")
full_links_list = set(soup.find_all("a", href=True))

document_links = [doc for doc in full_links_list if doc['href'].startswith("/cgi-bin/format.cgi?doc=")]
doc_id_links = []



for doc in document_links:
    doc_id = doc['href'].split('&')[0].split('doc=')[1].split('.')[0]
    doc_id_links.append(doc_id)

for link in doc_id_links:
    response = requests.get(BASE_URL + link + ".pdf", allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})
    save_path = os.path.join(".", "downloads", str(link).replace('/', '_') + '.pdf')
    if response.status_code != 200:
        response = requests.get(BASE_URL + link + ".rtf", allow_redirects=True,
                                headers={"User-Agent": "Chrome/102.0.0.0"})

        save_path = os.path.join(".", "downloads", str(link).replace('/', '_') + '.rtf')

        if response.status_code != 200:
            response = requests.get(BASE_URL + link + ".html", allow_redirects=True,
                                    headers={"User-Agent": "Chrome/102.0.0.0"})
            save_path = os.path.join(".", "downloads", str(link).replace('/', '_') + '.html')
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


print("sss")
