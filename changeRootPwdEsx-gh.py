from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import random
import string
from keepercommander.__main__ import get_params_from_config
from keepercommander.commands.record_edit import RecordUpdateCommand
from keepercommander import api

keeperParams = get_params_from_config("config.json")
api.login(keeperParams)
api.sync_down(keeperParams)

def generateRandomPassword(length):
    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SPECIAL_CHARS = "!@#$%^&*()-_+="
    all_chars = LOWERCASE + UPPERCASE + DIGITS + SPECIAL_CHARS
    secure_string = [
        random.choice(LOWERCASE),
        random.choice(UPPERCASE),
        random.choice(DIGITS),
        random.choice(SPECIAL_CHARS)
    ]
    remaining_length = length - len(secure_string) 
    for _ in range(remaining_length):
        secure_string.append(random.choice(all_chars))
    random.shuffle(secure_string)
    return "".join(secure_string)

def updateKeeperRecord(esxIP, passwordstr):
    record_search = api.search_records(keeperParams, esxIP)
    for record in record_search:
        if (routerIP == record.notes):
            print("found 1 keeper record matching search parameters: " + esxIP)
            print("Updating keeper record password to: " + passwordstr)
            RecordUpdateCommand().execute(keeperParams, record=record.record_uid, fields=['password=' + passwordstr])

def getKeeperPasswordForESX(esxIP):
    record_search = api.search_records(keeperParams, esxIP)
    for record in record_search:
        if (esxIP == record.notes):
            return ("" + record.password)
            #print("title:" + record.title, ", password:" + record.password, ", notes:" + record.notes)
        

esx_hosts = [
    "192.168.1.1",
    "192.168.1.2",
    "192.168.1.3",
]

for hostIP in esx_hosts:
    # Disable SSL verification for lab environments
    context = ssl._create_unverified_context()

    currentPassword = getKeeperPasswordForESX(hostIP)
    # Connect directly to ESXi or vCenter
    si = SmartConnect(
        host=hostIP,
        user="root",
        pwd=currentPassword,
        sslContext=context
    )

    content = si.RetrieveContent()
    # Get the HostSystem
    host = content.rootFolder.childEntity[0].hostFolder.childEntity[0].host[0]
    # Get the account manager for local users
    acct_mgr = host.configManager.accountManager
    # Create the required AccountSpecification object
    spec = vim.host.LocalAccountManager.AccountSpecification()
    spec.id = 'root'
    newpassword = generateRandomPassword(45)
    spec.password = newpassword

    # Update the user
    acct_mgr.UpdateUser(user=spec)

    Disconnect(si)
    print("Root password of host " + hostIP + " changed successfully to " + newpassword)
    updateKeeperRecord(hostIP,newpassword)
    
