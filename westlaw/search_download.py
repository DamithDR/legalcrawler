import requests
import json


def search_download(ran='1-50', srguid='', token=None,cookie=''):
    url = "https://launch.westlawasia.com/api/v1/deliveries/searches/download?range=" + ran

    payload = json.dumps({
        "format": "pdf",
        "predefinedRelationshipsType": "resultList",
        "srguid": srguid,
        "snippets": False,
        "highlight": False,
        "fulltext": True,
        "dsDisplay": "insolvency   ethics",
        "qryDisplay": "insolvency   ethics",
        "additionalParameters": {
            "summary": True,
            "links": True,
            "status": True,
            "sp": ""
        },
        "filename": "RTDoc"
    })
    headers = {
        'x-umu-token': token,
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://launch.westlawasia.com/resultlist',
        'sec-ch-ua-platform': '"Windows"',
        # 'Cookie': 'BIGipServerWLASIA-PROD-APP-9400=2175129098.47140.0000'
        'Cookie': cookie
    }

    response = requests.post(url, headers=headers, data=payload,allow_redirects=True)

    obj = json.loads(response.text)
    print(response.text)
    return obj['deliveryGuid']


if __name__ == '__main__':
    id = search_download(srguid='i0ad832f100000183a8ed215ea94ae724',
                         token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImZpcnN0TmFtZSI6IkRhbWl0aCIsImxhc3ROYW1lIjoiUHJlbWFzaXJpIiwiY2xpZW50SWQiOiJEYW1pdGgiLCJlbWFpbCI6IkQuUC5Eb2xhTXVsbGFnZUB3bHYuYWMudWsiLCJ0b2tlbiI6IldMVUstaTBhZDZhNTgxMDAwMDAxODNhOTA1MjA4MmJiNzhkNWRjIiwidXNlclR5cGUiOiJvbmVwYXNzIn0sImlhdCI6MTY2NDk4ODAyOSwiZXhwIjoxNjY0OTkxNjI5LCJhdWQiOiJVTVVfRnJvbnRFbmQiLCJpc3MiOiJVTVVfTWlkZGxld2FyZSJ9.eDpxJBwC8eXlRjS6cC0tNT2IsVaxssXATe_VFZz8Rd8')