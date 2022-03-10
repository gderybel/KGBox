# Payload source : https://github.com/payloadbox/xss-payload-list/blob/master/Intruder/xss-payload-list.txt
import requests

def LoadPayloads():
    file = open('payloads.txt', 'r')
    payloads = file.readlines()
    file.close()
    return payloads

def TestPayloads(payloads, target, parameter):
    for payload in payloads:
        #response = requests.get(target+payload)
        print(target+payload)


payloads = LoadPayloads()
TestPayloads(payloads, 'https://test.com/')