import requests


def download(token, document_id, save_path, cookie=''):
    url = "https://launch.westlawasia.com/api/v1/deliveries/" + document_id

    payload = {}
    headers = {
        'x-umu-token': token,
        'Accept': 'application/json, text/plain, */*',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'Referer': 'https://launch.westlawasia.com/resultlist',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Cookie': cookie
    }

    response = requests.get(url, headers=headers, data=payload, allow_redirects=True)

    if response.status_code == 200:
        print(save_path)
        with open(save_path, 'wb') as f:
            f.write(response.content)
    print("document download done : " + save_path)


if __name__ == '__main__':
    save_path = "downloads/test.pdf"
    download(save_path=save_path, document_id='i0ad6a58000000183a92b00fcb5e13f25',
             token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImZpcnN0TmFtZSI6IkRhbWl0aCIsImxhc3ROYW1lIjoiUHJlbWFzaXJpIiwiY2xpZW50SWQiOiJEYW1pdGgiLCJlbWFpbCI6IkQuUC5Eb2xhTXVsbGFnZUB3bHYuYWMudWsiLCJ0b2tlbiI6IldMVUstaTBhZDg5OGFhMDAwMDAxODNhOTI2MDIxM2I5NTNmYWM5IiwidXNlclR5cGUiOiJvbmVwYXNzIn0sImlhdCI6MTY2NDk5MDE4NCwiZXhwIjoxNjY0OTkzNzg0LCJhdWQiOiJVTVVfRnJvbnRFbmQiLCJpc3MiOiJVTVVfTWlkZGxld2FyZSJ9.oNykjAD7qkIQl7De1n80o2aV8xgkLNoAOSUQ5PMSuxw')
