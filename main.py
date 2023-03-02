import WindowsAudit
import CVESearch
import IPLocator
import LinkedinScrapper
import Whois

### HEADER ###

header = r"""
############################################# _ O X
#  ___  ____    ______  ______                    #
# |_  ||_  _| .' ___  ||_   _ \                   #
#   | |_/ /  / .'   \_|  | |_) |   .--.   _   __  #
#   |  __'.  | |   ____  |  __'. / .'`\ \[ \ [  ] #
#  _| |  \ \_\ `.___]  |_| |__) || \__. | > '  <  #
# |____||____|`._____.'|_______/  '.__.' [__]`\_] #
#                                                 #
###################################################
####### Guillaume de Rybel & Kylian Guihard #######
###################################################                                         
"""

print(header)

menu = r"""
1) Windows audit
2) CVE search
3) IP locator
4) Linkedin scrapper
5) Whois
6) Exit

Please choose a program to launch : 
"""

action = input(menu)

print('')

if action == '1':
    WindowsAudit.startProgram()
elif action == '2':
    CVESearch.startProgram()
elif action == '3':
    IPLocator.startProgram()
elif action == '4':
    LinkedinScrapper.startProgram()
elif action == '5':
    Whois.startProgram()
else:
    exit()

footer = r"""

###################################################
############# Thanks for using KGBox! #############
###################################################

"""

print(footer)

