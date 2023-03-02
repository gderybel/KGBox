import whois
import csv # work in progress
import re
import json
import dns
import os.path
from genericpath import exists
import whois

def Whois(domain):
    """
    This function will retrieve dns informations about a target IP/Domain.
    Requests are made through python-whois library.
    """
    domain_info = whois.whois(domain)

    if not all(domain_info.get(var) is None for var in domain_info):
        result = f"""
____________________________________________________________________________________________________________________________

[+]Domain: {domain_info.domain},
[+]Status: {domain_info.get('status')},
[+]Registrar: {domain_info.get('registrar')},
[+]Update time: {domain_info.get('updated_date')},
[+]Expiration time: {domain_info.get('expiration_date')},
[+]Servers names: {domain_info.get('name_servers')},
[+]Emails: {domain_info.get('emails')}

 ____________________________________________________________________________________________________________________________
"""
        print(result)

    else:
        print("\nTarget not valid.")
        exit()
    
    return domain_info


def outputToCsv(domain_info):
    """
    This function will output result to a csv file for further use.
    """
    csv_header = 'Domain,Status,Registrar,Update time,Expiration time,Servers names,Emails\n'
    csv_content = (
    str(domain_info.domain).replace(',',';') + ',' +
    str(domain_info.get('status')).replace(',',';') + ',' +
    str(domain_info.get('registrar')).replace(',',';') + ',' +
    str(domain_info.get('updated_date')).replace(',',';') + ',' +
    str(domain_info.get('expiration_date')).replace(',',';') + ',' +
    str(domain_info.get('servers_names')).replace(',',';') + ',' +
    str(domain_info.get('emails')).replace(',',';') +'\n'
    )

    filename = 'result.csv'

    if exists(filename):
        file = open('result.csv', 'a+')
        file.write(csv_content)
        file.close
    else:
        file = open('result.csv', 'w')
        file.write(csv_header + csv_content)
        file.close

def startProgram():
    domain = input('\nWelcome to our DNS loopkup tool ! Enter your target IP/Domain here : \n')
    domain_info = Whois(domain)

    # Output_file
    output = input('Would you like to save output to csv ? [y/N] : \n')
    if (output == 'y' or output == 'Y'):
        outputToCsv(domain_info)
    else:
        pass