import json
import requests
import sys

def CheckArguments():
    """
    This function will check arguments, and associate variable for future use.
    """
    output_argument = '-o'
    output = ''
    if output_argument in sys.argv:
        output = True

    no_output_argument = '-no'
    if no_output_argument in sys.argv:
        output = False

    ip_argument = '-ip'
    IP = ''
    if ip_argument in sys.argv:
        IP = sys.argv[sys.argv.index(ip_argument)+1]

    help_argument = '-h'
    if help_argument in sys.argv:
        print("""
        ---- Content ----

        -ip\tprecise IP to locate
        -h\tshow this help menu

        ---- Output ----

        -o\toutput result to ip-locator.csv
        -no\tno output
        """)
        exit()

    return output, IP

def findLocalisation(IP):
    url = f'https://ipinfo.io/{IP}/json'
    response = requests.get(url)
    if response.status_code != 200:
        print("\nCouldn't retreive information about this IP.\n")
        exit()
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

    return country, region, city, ISP, location

def OutputToCsv(country, region, city, ISP, location):
    file = open('ip-locator.csv', 'a')
    file.write(country+','+region+','+city+','+ISP+','+location+'\n')
    file.close()
    print("\nContent has been added to 'ip-locator.csv'.\n")

if __name__ == "__main__":
    output, IP = CheckArguments()

    if IP == '':
        IP = input("What's your IP address ? :\n")

    country, region, city, ISP, location = findLocalisation(IP)
    
    if output == '':
        output = input('Would you like to save data to a csv file ? (y/n) : \n')
        if output == 'y':
            output = True
        else:
            output = False
    
    if output:
        OutputToCsv(country, region, city, ISP, location)