
import random
import string
import os
import socket

def get_fqdn():
    fqdn = socket.getfqdn()
    if "localhost" in fqdn:
        fqdn = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET,
                                  socket.SOCK_DGRAM, socket.IPPROTO_IP,
                                  socket.AI_CANONNAME)[0][3]
        if "localhost" in fqdn:
            fqdn = socket.gethostname()
    return fqdn


TARGET = ""
CURDIR = os.getcwd()
RANDOMURL = "http://"+''.join(random.choice(string.ascii_letters) for i in range(12)) + random.choice([".settlers-outpost",
                           ".tech-dream",
                           ".mountainous-terrain",
                           ".highlife-extra",
                           ".school-session",
                           ".business-improvement",
                           ".superfluous",
                           ".extra-tedium",
                           ".testing-waters"])\
            +random.choice([".biz", ".net", ".org", ".com", ".tech", ".cn", ".fr"])
RANDOMURL_PS1 = random.choice(["https://raw.githubusercontent.com/PowerShellEmpire/PowerTools/master/PowerUp/PowerUp.ps1",
                 "https://raw.githubusercontent.com/sense-of-security/ADRecon/master/ADRecon.ps1",
                 "https://raw.githubusercontent.com/PowerShellEmpire/PowerTools/master/PowerView/powerview.ps1",
                 "https://raw.githubusercontent.com/BloodHoundAD/BloodHound/master/Ingestors/SharpHound.ps1",
                 "https://raw.githubusercontent.com/Kevin-Robertson/Inveigh/master/Inveigh.ps1",
                 "https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/privesc/Invoke-BypassUAC.ps1",
                 "https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Kerberoast.ps1",
                 "https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Mimikatz.ps1",
                 "https://raw.githubusercontent.com/PowerShellEmpire/PowerTools/master/PewPewPew/Invoke-MassMimikatz.ps1",
                 "https://raw.githubusercontent.com/besimorhino/Pause-Process/master/pause-process.ps1",
                 "https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Exfiltration/Get-Keystrokes.ps1",
                 "https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/collection/Get-ClipboardContents.ps1",
                 "https://raw.githubusercontent.com/Kevin-Robertson/Tater/master/Tater.ps1"
                 ])
RANDOMUSER = random.choice(["threatsim1", "simulating", "support_ast", "microsoft_test", "admin_test", "guest_user", "user_demo"])
RANDOMDOMAINUSER = []
RANDOMPORTUNCOMMON = random.choice([808, 880, 4050, 8000, 5190, 7900, 4443, 6789, 444, 8531, 4444, 50501, 8443, 9999])
RANDOMPORTCOMMON = random.choice([21, 22, 23, 25, 8080, 80, 137, 138, 139, 443, 445, 53, 23, 161, 502, 102, 1502])
FQDN = get_fqdn()
