# Payload source : https://github.com/payloadbox/xss-payload-list/blob/master/Intruder/xss-payload-list.txt

def LoadPayloads():
    file = open('payloads.txt', 'r')
    payloads = file.readlines()
    file.close()
    return payloads