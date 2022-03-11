# Payload source : https://github.com/payloadbox/xss-payload-list/blob/master/Intruder/xss-payload-list.txt
# Website : https://xss-game.appspot.com/level1/frame?query=

##### Tasks #####
# add user agent specification
# add output to csv
# try contact url before requests

import requests
import sys

def CheckArguments():
    """
    This function will check all arguments given by the user and assign values to variables.
    It permits to a user to not interact with the program (if all arguments are given).
    """
    useragent_argument = '-H'
    useragent = ''
    if useragent_argument in sys.argv:
        useragent = sys.argv[sys.argv.index(useragent_argument)+1]

    output_argument = '-o'
    output = ''
    if output_argument in sys.argv:
        output = True
    
    no_output_argument = '-no'
    if no_output_argument in sys.argv:
        output = False

    help_argument = '-h'
    if help_argument in sys.argv:
        print("""
        ---- Parameters ----

        -o\toutput result to a output.csv
        -no\tno output
        -H\tprecise the User-Agent to use, it might be betweeen quotes ''
        -h\tshow this help menu
        """)
        exit()

    return useragent, output
    

def LoadPayloads():
    file = open('payloads.txt', 'rb')
    payloads = file.readlines()
    file.close()
    return payloads

def TestPayloads(payloads, target, parameter, useragent, output):
    session = requests.session()
    if useragent == '':
        useragent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                            'AppleWebKit/605.1.15 (KHTML, like Gecko) '
                            'Version/15.2 Safari/605.1.15')
    session.headers.update({'User-Agent': useragent})

    if output == '':
        choice = input('Would you like to save output to a csv file ? (y/n) :\n')
        if choice == 'y':
            output = True
        else:
            output = False

    for payload in payloads:
        payload = payload.decode("utf-8").replace('\n','')
        payload_url = target+'?'+parameter+'='+payload
        response = session.get(payload_url)
        if str(payload) in response.text:
            print(f'Parameter "{parameter}" might be injectable with payload : "{payload}".')
            if output:
                OutputToCsv(payload,True)
        else:
            print(f'Parameter "{parameter}" might not be injectable.')
            if output:
                OutputToCsv(payload,False)


def OutputToCsv(payload,injectable):
    file = open('XSSScan.csv', 'a')
    file.write(f'{payload},{injectable}\n')
    file.close()

if __name__ == "__main__":
    useragent, output = CheckArguments()
    payloads = LoadPayloads()

    url = input('Wich URL shall we try to inject ? :\n')
    parameter = input('Wich URL parameter shall we try to inject ? :\n')
    TestPayloads(payloads, url, parameter, useragent, output)