import requests
import re
import sys
from getpass import getpass

def CheckArguments():
    """
    This function will check all arguments given by the user and assign values to variables.
    It permits to a user to not interact with the program (if all arguments are given).
    """
    output_argument = '-o'
    output = ''
    if output_argument in sys.argv:
        output = True
    
    no_output_argument = '-no'
    if no_output_argument in sys.argv:
        output = False

    company_argument = '-c'
    input_name = ''
    if company_argument in sys.argv:
        input_name = sys.argv[sys.argv.index(company_argument)+1]

    employees_counter = ''
    employees_counter_argument = '-ec'
    if employees_counter_argument in sys.argv:
        employees_counter = sys.argv[sys.argv.index(employees_counter_argument)+1]

    email = ''
    email_argument = '-e'
    if email_argument in sys.argv:
        email = sys.argv[sys.argv.index(email_argument)+1]

    password = ''
    password_argument = '-p'
    if password_argument in sys.argv:
        password = sys.argv[sys.argv.index(password_argument)+1]

    help_argument = '-h'
    if help_argument in sys.argv:
        print("""
        ---- Credentials ----

        -e\tprecise email to connect with Linkedin
        -p\tprecise password to connect with Linkedin, it might be between quotes

        Credentials are not saved to any distant server or anything, it's only used by the program.

        We don't recommand to use '-p' argument, because the plain text password could appear in command history

        ---- Parameters ----

        -o\toutput result to a output.csv
        -no\tno output
        -c\tprecise which company you want to retreive employees from (e.g. apple, uber-com, ...)
        -ec\tprecise how much employee should the program output (it has to be divisble by 25, default 25)
        -h\tshow this help menu
        """)
        exit()

    return email, password, input_name, employees_counter, output

def Login(email, password):
    """
    This function will connect user to Linkedin, grab session cookie and set headers to session, 
    for further use (Company & Employee requests).
    """
    session = requests.session()
    mobile_agent = ('Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 '
                        'Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) '
                        'Version/4.0 Mobile Safari/534.30')
    session.headers.update({'User-Agent': mobile_agent,
                                'X-RestLi-Protocol-Version': '2.0.0'})

    anon_response = session.get('https://www.linkedin.com/login')
    login_csrf = re.findall(r'name="loginCsrfParam" value="(.*?)"', anon_response.text)

    if email == '':
        email = input('\nWhat is your Linkedin email (Your account might have 10+ relations) : \n')

    if password == '':
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
            print(f"Couldn't connect, wrong redirection : {response.headers['Location']}\n")
            exit()
    except:
        print("Couldn't connect, credentials might be incorrect, or captcha was asked\n")
        exit()

    csrf_token = session.cookies['JSESSIONID'].replace('"', '')
    session.headers.update({'Csrf-Token': csrf_token})
    return session

def RetreiveCompanyInformations(session, input_name):
    """
    This function will retrieve Linkedin informations about a specified company.
    A company name can be found on it's Linkedin page url (e.g. : https://www.linkedin.com/company/microsoft/ => microsoft).
    Requests are made to Linkedin voyager API.
    """
    if input_name == '':
        input_name = input('Wich company ? (Name should be shown on company url, e.g : Uber=>uber-com, Apple=>apple, ...) : \n')

    company_response = session.get((f'https://www.linkedin.com/voyager/api/organization/companies?q=universalName&universalName={input_name}'))

    if company_response.status_code != 200:
        print("Please verify company name, couldn't retrieve data from it.\nYou can find a valid company name in the company Linkedin url (e.g. : https://www.linkedin.com/company/microsoft/ => microsoft).")
        exit()

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
        company_location = ('None','None','None')

    print('____________COMPANY DETAILS____________\n')
    print('Company name : %s'%company_name)
    print('Description : %s'%company_description)
    print('Website : %s'%company_website)
    print('Location : %s : %s, %s\n'%(company_location[2],company_location[1],company_location[0]))
    print('Staff : %s'%company_staff_count)

    return company_id

def RetreiveEmployeesInformations(session, employees_counter,company_id,output):
    """
    This function will retrieve employees information about a specified company.
    Number of employees retrieved has to be divisible by 25, if there are 106 employees in the company,
    and a user wants to retrieve all of them, he should indicate 125.
    """
    default_counter = 25
    if employees_counter == '':
        employees_counter = input(f'How many employees should we retreive ? It has to be divisible by 25 (default : {default_counter}) : \n')

    try:
        int(employees_counter)
    except:
        print(f"Invalid input, default value used ({default_counter})")
        employees_counter = default_counter

    if int(employees_counter)%25 == 0:
        starts = int(employees_counter)/25
    else:
        print('Number of employees has to be divisible by 25')
        exit()

    print('\n_____________ EMPLOYEES ______________\n')

    if output == '':
        output = input('Would you like to save data to a csv file ? (y/n) : \n')
        if output == 'y':
            output = True
        else:
            output = False

    for result in range(int(starts)):

        employees_response = session.get((f'https://www.linkedin.com/voyager/api/search/hits?facetCurrentCompany=List({company_id})&facetGeoRegion=List()&keywords=List()&q=people&maxFacetValues=15&supportedFacets=List(GEO_REGION,CURRENT_COMPANY)&count=25&origin=organization&start={result*25}'))

        if employees_response.status_code != 200:
            print("Please verify your network connection or status of Linkedin services, couldn't retreive data.")
            exit()

        employee_regex = r'firstName":"(.*?)","lastName":"(.*?)","dashEntityUrn":"urn:li:fsd_profile:(.*?)","occupation":"(.*?)"'

        employees = re.findall(employee_regex, employees_response.text)

        profile_url_header = "https://www.linkedin.com/profile/view?id="

        for employee in employees:
            print('Name : %s %s'%(employee[0], employee[1]))
            print('Role : %s'%employee[3])
            print('Link to profile : %s%s'%(profile_url_header,employee[2]))
            print('_________________________________\n')
            if output:
                file = open("output.csv", "a")
                file.write(str(employee[0].encode("ascii", "ignore").decode("utf-8") )+','+str(employee[1].encode("ascii", "ignore").decode("utf-8") )+','+str(employee[2].encode("ascii", "ignore").decode("utf-8") )+','+str(employee[3].encode("ascii", "ignore").decode("utf-8") )+'\n')
                file.close()
        
    if output:
         print('A csv file has been created : output.csv')

    print("\nIf there are a lot of blank names, it might be because your account is not old enough or doesn't have enough relations. In this case, Linkedin will keep people profile private just for you.\nIn this case, you should use another account because link to profile will not work aswell.\n")

email, password, input_name, employees_counter, output = CheckArguments()
session = Login(email, password)
company_id = RetreiveCompanyInformations(session, input_name)
RetreiveEmployeesInformations(session, employees_counter, company_id, output)