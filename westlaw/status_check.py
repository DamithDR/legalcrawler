import json

import requests


def check_status(id, token,cookie=''):
    url = "https://launch.westlawasia.com/api/v1/deliveries/" + id + "/status"

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Expires': '-1',
        'Pragma': 'no-cache',
        'Referer': 'https://launch.westlawasia.com/resultlist',
        'Host': 'launch.westlawasia.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-umu-token': token
    }

    response = requests.get(url, headers=headers, data=payload,allow_redirects=True)

    obj = json.loads(response.text)
    print(response.text)
    return obj['deliveryStatus']


# loop until : {"deliveryStatus":"DELIVERED"}
if __name__ == '__main__':
    check_status(id='i0ad6a58100000183a91b3b26bb78d789',
                 token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImZpcnN0TmFtZSI6IkRhbWl0aCIsImxhc3ROYW1lIjoiUHJlbWFzaXJpIiwiY2xpZW50SWQiOiJEYW1pdGgiLCJlbWFpbCI6IkQuUC5Eb2xhTXVsbGFnZUB3bHYuYWMudWsiLCJ0b2tlbiI6IldMVUstaTBhZDZhNTgxMDAwMDAxODNhOTA1MjA4MmJiNzhkNWRjIiwidXNlclR5cGUiOiJvbmVwYXNzIn0sImlhdCI6MTY2NDk4ODAyOSwiZXhwIjoxNjY0OTkxNjI5LCJhdWQiOiJVTVVfRnJvbnRFbmQiLCJpc3MiOiJVTVVfTWlkZGxld2FyZSJ9.eDpxJBwC8eXlRjS6cC0tNT2IsVaxssXATe_VFZz8Rd8')
