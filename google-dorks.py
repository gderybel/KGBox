from urllib import request
from bs4 import BeautifulSoup
import requests

# je contacte l'URL contenant les dorks de référence"
def URL_google_dorks():

    url = "https://www.exploit-db.com/google-hacking-database"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "deflate, gzip, br",
        "Accept-Language": "en-US",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "X-Requested-With": "XMLHttpRequest",
    }


    print(f"[+] requete en cours sur l'URL: {url}")
    request = requests.get(url, headers=headers)

    if request.status_code != 200:
        print("l'URL n'est pas joignable. Veuillez vérifier votre URL")
        return
    else:
        print("l'URL est bien joignable (code 200)")
        return

URL_google_dorks()