import codecs
import json
import time

import requests

from westlaw.download_file import download
from westlaw.search_download import search_download
from westlaw.status_check import check_status

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImZpcnN0TmFtZSI6IkRhbWl0aCIsImxhc3ROYW1lIjoiUHJlbWFzaXJpIiwiZW1haWwiOiJELlAuRG9sYU11bGxhZ2VAd2x2LmFjLnVrIiwidG9rZW4iOiJXTFVLLWkwYWQ4OThhNjAwMDAwMTgzYzE0YTRkNGExOTIxMTM0YiIsInVzZXJUeXBlIjoib25lcGFzcyJ9LCJpYXQiOjE2NjUzOTUyMTUsImV4cCI6MTY2NTM5ODgxNSwiYXVkIjoiVU1VX0Zyb250RW5kIiwiaXNzIjoiVU1VX01pZGRsZXdhcmUifQ.cY09IVPeITPmBJC9jwNbV4kHQ6q2aVdgM8VEQmYRlh0"
COOKIE = "BIGipServerWLASIA-PROD-APP-9400=2158351882.47140.0000"


def run():
    query_list = [
        # "insolvency ethics",
        "insolvency ethical behavior",
        "insolvency code of ethics",
        "insolvency practitioner",
        "insolvency liquidator",
        "insolvency misconduct",
        "insolvency Lack of impartiality",
        "insolvency Breach of duty of care",
        "insolvency Standards of conduct",
        "insolvency Code of conduct"
    ]
    # australia, hong kong, india, malaysia, new zealand, singapore, uk
    countries = [
        # "au",
        # "hk",
        # "in",
        # "my",
        # "nz",
        "sg"
    ]

    print('starting crawling')

    for country in countries:
        print('crawling country ' + country)
        for query in query_list:
            print('crawling search term ' + query)
            SEARCH_URL = "https://launch.westlawasia.com/api/v1/documents/search"
            payload = json.dumps({
                "sttype": "nl",
                "searchtype": "",
                "stid": "std-wla-searchall",
                "country": [
                    country
                ],
                "infotype": [
                    "cases-temp-ds"
                ],
                "practiceArea": "",
                "frt_srch": query,
                "snippets": True
            })

            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Cookie': COOKIE,
                'Origin': 'https://launch.westlawasia.com',
                'Referer': 'https://launch.westlawasia.com/search?tocguid=IAED6CC08DD364059AB193CEAF31A4AB0',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'x-umu-token': TOKEN
            }
            payload = requests.post(SEARCH_URL, allow_redirects=True, headers=headers, data=payload)

            string = codecs.decode(payload.content, payload.encoding)
            fields = json.loads(string)
            no_of_documents = int(fields['documentCount'])
            print('no of documents found ' + str(no_of_documents))

            start_point = 1
            end_point = 50
            batch_size = 50
            if end_point > no_of_documents:
                end_point = no_of_documents

            while end_point <= no_of_documents and start_point < no_of_documents:
                ran = str(start_point) + '-' + str(end_point)
                print('preparing document ' + ran)
                download_id = search_download(srguid=fields['searchResultHandle'], ran=ran,
                                              token=TOKEN, cookie=COOKIE)

                print('document status check starting')
                status = check_status(id=download_id, token=TOKEN, cookie=COOKIE)

                req_counter = 0

                while not 'DELIVERED'.__eq__(status) and req_counter < 120:
                    status = check_status(id=download_id, token=TOKEN, cookie=COOKIE)
                    req_counter += 1
                    time.sleep(3)  # wait for 1 second
                print('document status check done')

                save_path = 'downloads/' + country + '/' + query + ran + ".pdf"
                download(token=TOKEN, document_id=download_id, save_path=save_path, cookie=COOKIE)

                start_point += batch_size
                end_point += batch_size
                if end_point > no_of_documents:
                    end_point = no_of_documents


if __name__ == '__main__':
    run()
