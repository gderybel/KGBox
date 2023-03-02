# KGBox

This toolbox is a project made by Guillaume de Rybel & Kylian Guihard for a Master School project.

The objective of the project is defined in the research and the collection of specific information.

We developed 5 tools for this project:
- LinkedinScrapper
- CVE search
- IPLocator
- Whois
- WindowsAudit

Whois, IPLocator and LinkedinScrapper are OSINT tools, while CVEsearch and WindowsAudit are security tools.
We oriented our toolbox to output results to csv files, for further use.

We use 4 not installed python librairies : 
- requests
- pandas
- python-whois
- dnspython

You can install them easily by typing : 

	pip install -r requirements.txt

___

## LinkedinScrapper
Linkedin Scrapper is a tool that can retrieve every employee of a given company, and output result to csv for further use (username guessing, information gathering, ...).

It will ask for your **personal account informations** (email & password) to retrieve your session and use it with Linkedin Voyager API. No one will see that you "visited" any user profile. **No session information is saved.**

## CVE search
CVE search is a program that retrieve any CVE from Mitre downloads (https://cve.mitre.org/data/downloads/allitems.csv). It performs fast searches with pandas dataframes, you can search by Author, CVE id and description.

## IP Locator
This tool will simply retrieve an IP location from ipinfo website (https://ipinfo.io/{IP}/json). Result can be outputted to a csv file.

## Whois
This program will search for domain informations such as update and expiration dates, admin emails and servers names. Every result can be outputted to csv file.

## WindowsAudit
**This tool can only be run on Windows Systems.**\

This security tool will audit your computer and look for high security risk (CIS) hardening policies. It can be useful for a striker to detect vulnerabilities or a defender to patch computers. It uses native windows tools. **It has to be run as admin to have every result and PowerShell execution have to be enabled.**

Policies concerned:
- 1.1.7 - Store passwords using reversible encryption
- 2.3.11.5 - Network security: Do not store LAN Manager hash value on next password change
- 18.3.6 - WDigest Authentication
- 18.6.2 - Point and Print Restrictions: When installing drivers for a new connection
- 18.6.3 - Point and Print Restrictions: When updating drivers for an existing connection
- 18.3.2 - Configure SMB v1 client driver
- 18.9.45.8.2 - Real-time Protection: Turn off real-time protection
- Check Bitlocker status

CIS recommendations can be found here https://learn.cisecurity.org/l/799323/2022-02-07/qdwwc, used policies are not from the most recent CIS benchmark version.
