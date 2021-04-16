#!/usr/bin/env python3
import requests
from urllib.parse import urlparse, parse_qs
import os

s = requests.Session()
test_password = os.getenv('TEST_PASSWORD')
test_username = os.getenv('TEST_USERNAME')

url = "https://web-stage.learnin2432.com/auth/Account/Login?ReturnUrl=%2Fauth%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dtoken%2520id_token%26nonce%3D98765%26state%26client_id%3Dstackhawk%26scope%3Dopenid%26redirect_uri%3Dhttps%253A%252F%252Fjwt.ms"
payload = {
    "Email": test_username,
    "Password": test_password,
}

r = s.post(url, data=payload, allow_redirects=True)

tokenUrl = r.url
query = parse_qs(tokenUrl)
token = query['https://jwt.ms#id_token'][0]

if os.getenv('GITHUB_ACTIONS') == 'true':
    github_environment_file = os.getenv('GITHUB_ENV')
    with open(github_environment_file, 'a') as file_handle:
        file_handle.write("\n")
        file_handle.write("ID_TOKEN=" + token)

print("For reference, here is the authentication token:")
print(token)
