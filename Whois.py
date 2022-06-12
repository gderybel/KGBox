import whois
import csv # work in progress
import re
import json
import dns
import os.path

def Whois():

    print('Bienvenue dans le programme DNS Lookup de KGBox ! Renseigne ici le domaine que tu souhaites cibler:')
    domain_info = whois.whois(input())
    
    if len(domain_info) != 0: # need to work the condition
                        # Result
        f = ("[+]Domain: ", domain_info.domain,
            "\n[+]Status: ", domain_info.get('status'),
            "\n[+]Registrar: ", domain_info.get('registrar'),
            "\n[+]Update time: ", domain_info.get('updated_date'),
            "\n[+]Expiration time: ", domain_info.get('expiration_date'),
            "\n[+]Name server: ", domain_info.get('name_servers'),
            "\n[+]Email: ", domain_info.get('emails'))
        fstr = str(f)
        file = open('result.txt', 'a+')
        file.write(fstr)
        file.readlines()
        file.close

                        # Output_file
        """print('souhaitez-vous enregistrer ses informations dans un fichier TXT [o/N]')

        if input() == 'o':
            save_path = 'C:/'
            file = open('result.txt', 'w')
            #modifier le file.write ci dessous
            file.write(str(domain_info.domain.encode("ascii", "ignore").decode("utf-8")))
            file.close()
        else:
            pass"""
    else:
        print("Le domaine renseigné n'est pas valide. vérifiez l'orthographe puis réessayez.")


Whois()