from bs4 import BeautifulSoup

import requests

from common.utils import Extension
from common.utils.utility import download_file

DOWNLOAD_BASE_URL = "https://www.elitigation.sg/gd/gd/"


# def download_links(doc_id_links=[]):
#     for link in doc_id_links:
#         response, save_path = download_file(base_url=DOWNLOAD_BASE_URL, link=link,
#                                             extension=Extension.Extension.SlashPDF.value)
#         if response.status_code != 200:
#             response, save_path = download_file(base_url=DOWNLOAD_BASE_URL, link=link, extension=Extension.RTF.value)
#             if response.status_code != 200:
#                 response, save_path = download_file(base_url=DOWNLOAD_BASE_URL, link=link,
#                                                     extension=Extension.HTML.value)
#                 if response.status_code != 200:
#                     print("cannot find the pdf, rtf or html document for document link : " + link)
#         if response.status_code == 200:
#             print(save_path)
#             with open(save_path, 'wb') as f:
#                 f.write(response.content)


def extract_and_download(query, start_rank=1):
    SEARCH_URL = "https://search2.fedcourt.gov.au/s/search.html?collection=judgments&sort=date&meta_v_phrase_orsand=judgments%2FJudgments%2F&meta_2=&meta_A=&meta_z=&meta_3=&meta_n_phrase_orsand=&query_sand=" \
                 + query + "&query_or=&query_not=&query_phrase=&query_prox=&meta_d=&meta_d1=&meta_d2=&meta_7=&meta_4=&meta_B=&start_rank=" + str(
        start_rank)
    payload = requests.get(SEARCH_URL, allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})
    soup = BeautifulSoup(payload.content, "html.parser")
    full_links_list = set(soup.find_all("a", href=True))

    document_links = [doc for doc in full_links_list if doc['href'].__contains__("/judgments/Judgments/")]
    for doc in document_links:
        doc_payload = requests.get(doc['href'], allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})
        doc_soup = BeautifulSoup(doc_payload.content, "html.parser")
        loaded_doc = set(doc_soup.find_all("a", href=True))

        for lnk in loaded_doc:
            if lnk.contents[0].__contains__("Original Word Document"):
                split = lnk['href'].split('/')
                link = split[len(split) - 1]
                version = link.split('v=')[1]
                doc_link = link.split('v=')[0].split('.')[0]
                extention = '.' + link.split('v=')[0].split('.')[1].replace('?', '')
                base_url = '/'.join(split[0:len(split) - 1]) + '/'
                response, save_path = download_file(base_url=base_url, link=doc_link, extension=extention,
                                                    version=version)
                if response.status_code == 200:
                    print(save_path)
                    with open(save_path, 'wb') as f:
                        f.write(response.content)

    return payload


def run():
    query_list = [
        "insolvency+ethics",
        "insolvency+ethical behavior",
        "insolvency+code of ethics",
        "insolvency+practitioner",
        "insolvency+liquidator",
        "insolvency+misconduct",
        "insolvency+Lack of impartiality",
        "insolvency+Breach of duty of care",
        "insolvency+Standards of conduct",
        "insolvency+Code of conduct"
    ]

    for query in query_list:

        SEARCH_URL = "https://search2.fedcourt.gov.au/s/search.html?collection=judgments&sort=date&meta_v_phrase_orsand=judgments%2FJudgments%2F&meta_2=&meta_A=&meta_z=&meta_3=&meta_n_phrase_orsand=&query_sand=" + query + "&query_or=&query_not=&query_phrase=&query_prox=&meta_d=&meta_d1=&meta_d2=&meta_7=&meta_4=&meta_B="
        payload = requests.get(SEARCH_URL, allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})

        soup = BeautifulSoup(payload.content, "html.parser")
        full_links_list = set(soup.find_all("a", href=True))

        document_links = [doc for doc in full_links_list if doc['href'].__contains__("/judgments/Judgments/")]
        pagination_links = [page for page in full_links_list if
                            page['href'].__contains__("start_rank=")]

        page_numbers = [1]
        for page in pagination_links:
            content = page.contents
            arr = page.attrs['href'].split('&')
            for split in arr:
                for cont in content:
                    if split.startswith('start_rank') and cont.isdigit():
                        page_numbers.append(int(split.split('=')[1]))

        for num in page_numbers:
            extract_and_download(query, num)


if __name__ == '__main__':
    run()
