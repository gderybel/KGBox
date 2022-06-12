from winreg import *
from subprocess import *
import platform
import ctypes
import re
import os

def CheckOs():
    return platform.system()

def CheckIfRoot():
    return ctypes.windll.shell32.IsUserAnAdmin()

def GetRegistryValue(path, keyname):
    cmd = "powershell -Command Get-ItemPropertyValue -Path '" + path + "' -Name " + keyname
    with Popen(cmd, stdout=PIPE, stderr=None, shell=True) as process:
        try:
            return process.communicate()[0].decode("utf-8")[0]
        except:
            return None

def CheckSMBv1Support():
    cmd = "Get-WindowsOptionalFeature -Online -FeatureName smb1protocol"
    smbv1 = run(["powershell", "-Command", cmd], capture_output=True)
    smbv1_result = re.search(r'(?<=State            : )[^.\\]*',str(smbv1))
    if smbv1_result:
        return smbv1_result.group(0)
    else:
        return 'Not found (Default value : Disabled)'

def CheckStorePasswordUsingReversibleEncryption():
    secedit_output_file = 'secedit_ouput'
    run(['secedit', '/export', '/cfg', secedit_output_file, '/areas', 'SECURITYPOLICY'], stdout=DEVNULL, stderr=DEVNULL)
    file = open(secedit_output_file, "r")
    content = file.read()
    formatted_content = content.replace('\x00','')
    revesible_encryption_result = re.search(r'(?<=ClearTextPassword = )[^.\n]*',str(formatted_content))
    file.close()
    os.remove(secedit_output_file)
    if revesible_encryption_result:
        if revesible_encryption_result.group(0) == '0':
            return 'Disabled'
        elif revesible_encryption_result.group(0) == '1':
            return 'Enabled'
        else:
            return 'Not found (Default value : Disabled)'
    else:
        return 'Not found (Default value : Disabled)'

def CheckStoreLMHashValue():
    path = "HKLM:\System\CurrentControlSet\Control\Lsa"
    keyname = "NoLMHash"
    value = GetRegistryValue(path, keyname)
    if value == '1':
        return 'Enabled'
    elif value == '0':
        return 'Disabled'
    else:
        return 'Not found (Default value : Enabled)'

def CheckPrinterDriverNewConnectionCVE202134527():
    path = "HKLM:\SOFTWARE\Policies\Microsoft\Windows NT\Printers\PointAndPrint"
    keyname = "NoWarningNoElevationOnInstall"
    value = GetRegistryValue(path, keyname)
    if value == '1':
        return 'Enabled'
    elif value == '0':
        return 'Disabled'
    else:
        return 'Not found (Default value : Disabled)'

def CheckPrinterDriverExistingConnectionCVE202134527():
    path = "HKLM:\SOFTWARE\Policies\Microsoft\Windows NT\Printers\PointAndPrint"
    keyname = "UpdatePromptSettings"
    value = GetRegistryValue(path, keyname)
    if value == '1':
        return 'Enabled'
    elif value == '0':
        return 'Disabled'
    else:
        return 'Not found (Default value : Disabled)'

def CheckBitlockerStatus():
    cmd = "Get-BitLockerVolume -MountPoint C: | Format-List"
    smbv1 = run(["powershell", "-Command", cmd], capture_output=True)
    smbv1_result = re.search(r'(?<=VolumeStatus         : )[^.\\]*',str(smbv1))
    if smbv1_result:
        return smbv1_result.group(0)
    else:
        return 'Not found (Default value : FullyDecrypted)'

def CheckWDigestAuthentication():
    path = "HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest"
    keyname = "UseLogonCredential"
    value = GetRegistryValue(path, keyname)
    if value == '1':
        return 'Enabled'
    elif value == '0':
        return 'Disabled'
    else:
        return 'Not found (Default value : Disabled)'

def CheckRealTimeMonitoring():
    cmd = "Get-MpPreference"
    smbv1 = run(["powershell", "-Command", cmd], capture_output=True)
    smbv1_result = re.search(r'(?<=DisableRealtimeMonitoring                     : )[^.\\]*',str(smbv1))
    if smbv1_result:
        return smbv1_result.group(0)
    else:
        return 'Not found (Default value : False)'

if CheckOs() == "Windows":
    if CheckIfRoot():
        print('SMBv1 Support : ' + CheckSMBv1Support())
        print('Store passwords using reversible encryption : ' + CheckStorePasswordUsingReversibleEncryption())
        print('BitLocker Drive Encryption: Volume status : ' + CheckBitlockerStatus())
    else: 
        print("User not admin, skipping SMBv1 Support, Store passwords using reversible encryption and BitLocker Drive Encryption: Volume status.")
    print('Network security: Do not store LAN Manager hash value on next password change : ' + CheckStoreLMHashValue())
    print('Point and Print Restrictions: When installing drivers for a new connection (CVE-2021-34527) : ' + CheckPrinterDriverNewConnectionCVE202134527())
    print('Point and Print Restrictions: When updating drivers for an existing connection (CVE-2021-34527) : ' + CheckPrinterDriverExistingConnectionCVE202134527())
    print('WDigest Authentication : ' + CheckWDigestAuthentication())
    print('Real time monitoring : ' + CheckRealTimeMonitoring())

else:
    print('This program is only available on Windows.')