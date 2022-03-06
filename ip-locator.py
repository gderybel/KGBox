import json
import requests

def findLocalisation(IP):
    url = 'http://ipinfo.io/json'
    response = requests.get(url)
    data = json.loads(response.text)

    ISP=data['org']
    city = data['city']
    country=data['country']
    region=data['region']
    location=data['loc']

    print(f"""
Your IP detail

   Country : {country}, {region}, {city}
   ISP : {ISP}
   Location : {location}
   """)

IP = input("What's your IP address ? :\n")
findLocalisation(IP)