import requests
import re
import sys
from getpass import getpass

company_argument = '-c'
if company_argument in sys.argv:
    input_name = sys.argv[sys.argv.index(company_argument)+1]

email_argument = '-e'
if email_argument in sys.argv:
    email = sys.argv[sys.argv.index(email_argument)+1]

password_argument = '-p'
if password_argument in sys.argv:
    password = sys.argv[sys.argv.index(password_argument)+1]

help_argument = '-h'
if help_argument in sys.argv:
    print("""
    ---- Credentials ----

    -e\tprecise email to connect with Linkedin
    -p\tprecise password to connect with Linkedin

    Credentials are not saved to any distant server or anything, it's only used by the program.

    We don't recommand to use '-p' argument, because the plain text password could appear in command history

    ---- Parameters ----

    -c\tprecise which company you want to retreive employees from (e.g. apple, uber-com, ...)
    -h\tshow this help menu
    """)
    exit()


session = requests.session()
mobile_agent = ('Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 '
                    'Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) '
                    'Version/4.0 Mobile Safari/534.30')
session.headers.update({'User-Agent': mobile_agent,
                            'X-RestLi-Protocol-Version': '2.0.0'})

anon_response = session.get('https://www.linkedin.com/login')
login_csrf = re.findall(r'name="loginCsrfParam" value="(.*?)"', anon_response.text)

if 'email' not in globals():
    email = input('\nWhat is your Linkedin email (Your account might have 10+ relations) : \n')

if 'password' not in globals():
    password = getpass('Enter your password : \n')

auth_payload = {
        'session_key': email,
        'session_password': password,
        'isJsEnabled': 'false',
        'loginCsrfParam': login_csrf
    }

response = session.post('https://www.linkedin.com/checkpoint/lg/login-submit?loginSubmitSource=GUEST_HOME', data=auth_payload, allow_redirects=False)

try:
    if response.headers['Location'] == 'https://www.linkedin.com/feed/':
        print('Connected Successfully\n')
    else:
        print("Couldn't connect, wrong redirection\n")
        exit()
except:
    print("Couldn't connect, credentials might be incorrect\n")
    exit()

csrf_token = session.cookies['JSESSIONID'].replace('"', '')
session.headers.update({'Csrf-Token': csrf_token})

if 'input_name' not in globals():
    input_name = input('Wich company ? (Name should be shown on company url, e.g : Uber=>uber-com, Apple=>apple, ...) : \n')

company_response = session.get(('https://www.linkedin.com/voyager/api/organization/companies?q=universalName&universalName='+input_name))

website_regex = r'companyPageUrl":"(http.*?)"'
name_regex = r'"name":"(.*?)"'
staff_regex = r'staffCount":([0-9]+),'
id_regex = r'"objectUrn":"urn:li:company:([0-9]+)"'
desc_regex = r'tagline":"(.*?)"'
location_regex = r'"streetAddressOptOut":true,"country":"(.*?)","city":"(.*?)","headquarter":true,"description":"(.*?)"}]}]'

try:
    company_id = re.findall(id_regex, company_response.text)[0]
except:
    company_id = 'None'
try:
    company_name = re.findall(name_regex, company_response.text)[0]
except:
    company_name = 'None'
try:
    company_staff_count = re.findall(staff_regex, company_response.text)[0]
except:
    company_staff_count = 'None'
try:
    company_website = re.findall(website_regex, company_response.text)[0]
except:
    company_website = 'None'
try:
    company_description = re.findall(desc_regex, company_response.text)[0]
except:
    company_description = 'None'
try:
    company_location = re.findall(location_regex, company_response.text)[0]
except:
    company_location = 'None'

print('\nCOMPANY DETAILS\n')
print('Company name : %s'%company_name)
print('Description : %s'%company_description)
print('Website : %s'%company_website)
print('Location : %s : %s, %s\n'%(company_location[2],company_location[1],company_location[0]))
print('Staff : %s'%company_staff_count)

employees_response = session.get(('https://www.linkedin.com/voyager/api/search/hits?facetCurrentCompany=List('+ company_id +')&facetGeoRegion=List()&keywords=List()&q=people&maxFacetValues=15&supportedFacets=List(GEO_REGION,CURRENT_COMPANY)&count=25&origin=organization&start=0'))

employee_regex = r'firstName":"(.*?)","lastName":"(.*?)","dashEntityUrn":"urn:li:fsd_profile:(.*?)","occupation":"(.*?)"'

employees = re.findall(employee_regex, employees_response.text)

profile_url_header = "https://www.linkedin.com/profile/view?id="
print('_____________ Employees ______________\n')

for employee in employees:
    print('Name : %s %s'%(employee[0], employee[1]))
    print('Role : %s'%employee[3])
    print('Link to profile : %s%s'%(profile_url_header,employee[2]))
    print('_________________________________\n')