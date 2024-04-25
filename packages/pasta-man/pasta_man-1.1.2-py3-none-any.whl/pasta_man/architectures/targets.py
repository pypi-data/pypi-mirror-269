#
# This file is an architecture for all operations
#

# import project specific modules.
from pasta_man.utilities.Exceptions.exceptions import InvalidKeyword, InvalidExportType, InvalidImportType
from pasta_man.utilities.retransform import Retransform

# import other arguments
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode
from pathlib import Path
from os import getcwd as pwd
from os.path import join as jPath, exists as there
from datetime import datetime
import pandas as pd
import sys

#
# The format to save the persistent passwords file ==>
# key:value|key:value|...\n
#
#

class targets:
    def __init__(self, masterpassword: bytes):
        """Initialize targets class.

        Args:
            masterpassword (bytes): master password encoded in 'ascii'
            mastersalt (bytes, optional): master salt encoded in 'ascii'. Defaults to "pastaman".encode('ascii').
        
        Description:
            masterpassword: The Password to Encrypt All. To encode in bytes, use <password-value>.encode('ascii')
            mastersalt: Salt is addition text to strengthen the password. By default it is set to 'pastaman'. To encode in bytes, use <salt-text>.encode('ascii')
        """
        # initialize data
        self.data:list[dict] = []
        self.msalt = "pastaman".encode('ascii')
        self.mpass = masterpassword
    
    def init(self):
        # create kdf object
        _kdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            iterations=480000,
            salt=self.msalt,
        )
        
        # derive password digest
        self.passwd = urlsafe_b64encode(_kdf.derive(self.mpass))
        
        # define fernet object
        self.fernet = Fernet(self.passwd)
        
        # check for pre-existing config files => for persistent memory
        # -> if not found, create
        # --> store home path
        home = str(Path.home())
        
        # if config file present, else create an init entry.
        if there(jPath(home, '.pastaman', '.passwords')):
            # open passwords file
            with open(jPath(home, '.pastaman', '.passwords'), 'rb') as p:
                content = p.read()
            # decrypt passwords file
            content = self.fernet.decrypt(content)
            
            # divide content based on lines
            content = content.decode('ascii').split('\n')
            
            # for each line add the data to self.data
            for x in content:
                if x=="":
                    continue
                # split key-value pairs
                x = x.split('|') # [k:v, k:v, ...]
                # for each key-value pair, store key and value
                # -> in data
                data = {}
                for kv in x:
                    # split keys and values
                    kv = kv.split(':')
                    data[kv[0]] = kv[1]
                
                self.data.append(data)
            
            content = None
        else:
            # create a .passwordsfile
            with open(jPath(home, ".pastaman", '.passwords'), 'w') as pfile:
                pfile.write(f"target-type:init|target:init|username:init|password:{self.fernet.encrypt('init'.encode('ascii')).decode('ascii')}|timestamp:{datetime.today().strftime('%Y-%m-%d')}\n")
            
            with open(jPath(home, ".pastaman", '.passwords'), 'rb') as p:
                content = p.read()
            
            content = self.fernet.encrypt(content)
            
            with open(jPath(home, ".pastaman", '.passwords'), 'wb') as pfile:
                pfile.write(content)
            
            content = None
        
        sys.exit(0)
        
    def __append(self, data: list[dict]):
        # append to data variable
        self.data.extend(data)
        
        # read current data
        with open(jPath(str(Path.home()), '.pastaman', '.passwords'), 'rb') as pfile:
            __content = pfile.read()
        
        # decrypt
        __content = self.fernet.decrypt(__content).decode('ascii').split('\n')
        
        # add the lines
        for dictionary in data:
            string = "target-type:"+dictionary['target-type']+"|target:"+dictionary['target']+"|username:"+dictionary['username']+"|password:"+dictionary['password']+"|timestamp:"+dictionary['timestamp']
            __content.append(string)
        
        __contentstring = ""
        for x in __content:
            __contentstring += x + "\n"
        
        __contentstring = self.fernet.encrypt(__contentstring.encode('ascii'))
        
        with open(jPath(str(Path.home()), '.pastaman', '.passwords'), 'wb') as pfile:
            pfile.write(__contentstring)
    
    def add(self, target:str, targettype: str, username: str, password:bytes):
        """Add data in collection.

        Args:
            target (str): target is the place where this data is valid.
            targettype (str): example -> link, app, etc.
            username (str): credential
            password (bytes): password in bytes. Encoding -> 'ascii'
        """
        # set date time format
        t = datetime.today().strftime("%Y-%m-%d")
        
        # define data instance
        data = {
            "target-type":targettype,
            "target":target,
            "username":username,
            "password":self.fernet.encrypt(password),
            "timestamp":t
        }
        
        # append to self.data for safe keeping
        self.data.append(data)
        
        # create the string to be written in .passwords file
        pstring = "target-type:"+targettype+'|'+"target:"+target+'|'+"username:"+username+'|'+"password:"+self.fernet.encrypt(password).decode('ascii')+"|"+"timestamp:"+t
        
        # decrypt the passwords file
        # -> read it
        with open(jPath(str(Path.home()), ".pastaman", '.passwords'), 'rb') as pfile:
            content = pfile.read()
        
        # decrypt
        content = self.fernet.decrypt(content)
        
        # add entry
        content = content.decode('ascii').split('\n') # split by lines
        content.append(pstring)
        
        pstring = None
        
        # generate the string again
        newcontent = ""
        for x in content:
            newcontent += x + "\n"
        
        content = None
        
        newcontent = self.fernet.encrypt(newcontent.encode('ascii'))
        
        # write it
        with open(jPath(str(Path.home()), '.pastaman', '.passwords'), 'wb') as pfile:
            pfile.write(newcontent)
        
        newcontent = None
        
        sys.exit(0)
    
    def remove(self, target:str, username: str):
        """remove an entry from the collection of all entries.

        Args:
            target (str): target name.
            username (str): username.
        """
        for dictionary in self.data:
            if dictionary['target']==target and dictionary['username']==username:
                dump = self.data.pop(self.data.index(dictionary))
                dump = None
    
    def authenticate(self, username: str ,password: bytes) -> bool:
        """check if the username has the given password

        Args:
            username (str): username 
            password (bytes): password encoded in 'ascii'. To encode in ascii, use -> <password-text>.encode('ascii')

        Returns:
            bool: True if authentication passes, else False.
        """
        for dictionary in self.data:
            if dictionary['username']==username and dictionary['password']==self.fernet.encrypt(password):
                return True
        
        return False
    
    def count(self) -> dict:
        """Dynamic count of all target-types

        Returns:
            dict: returns a dictionary with target-types as keys and their counts as their values.
        
        Description:
            Example Output:
                1. {
                    "target-type_1":23,
                    "target-type_2":10,
                    ...
                }
                
                2. {} -> could be an empty dict.
        """
        counts:dict = {}
        count_target_types: int = 0
        counted_targets: list[str] = []
        for dictionary in self.data:
            if dictionary['target-type'] not in counted_targets:
                count_target_types += 1
                counted_targets.append(dictionary['target-type'])
        
        count = 0
        for targettype in counted_targets:
            for dictionary in self.data:
                if dictionary['target-type'] == targettype:
                    count += 1
            
            counts[targettype] = count
            count = 0
        
        return counts
    
    def search(self, searchkeyword: str, keywordtype: str = "target"):
        """search an entry by these keywordtypes -> ['target', 'target-type', 'username']

        Args:
            searchkeyword (str): _description_
            keywordtype (str, optional): _description_. Defaults to "target".
        """
        valid = ['target', 'target-type', 'username']
        
        if keywordtype not in valid:
            raise InvalidKeyword(f'{keywordtype} cannot be set as keywordtype.')
        
        self.__searchresult__ = None
        
        for dictionary in self.data:
            if searchkeyword in dictionary[keywordtype]:
                self.__searchresult__ = dictionary
        
        sys.exit(0)
    
    def searchAll(self, searchkeyword:str, keywordtype: str = "target"):
        valid = ['target', 'target-type', 'username']
        
        if keywordtype not in valid:
            raise InvalidKeyword(f'{keywordtype} cannot be set as keywordtype.')
        
        self.__searchAllResult = []
        
        for dictionary in self.data:
            if searchkeyword in dictionary[keywordtype]:
                self.__searchAllResult.append(dictionary)
    
    def __fetchSearchAll(self):
        return self.__searchAllResult
    
    searchAllResults = property(fget=__fetchSearchAll)

    def targets(self):
        ts:list[str] = []
        added = []
        for dictionary in self.data:
            if dictionary['target-type']!="init" and dictionary['target-type'] not in added:
                ts.append(dictionary['target-type'])
                added.append(dictionary['target-type'])
        
        self.__target_types__ = ts
    
    def decrypt(self, password: bytes):
        self.dec = self.fernet.decrypt(password).decode('ascii')
        sys.exit(0)
    
    def export(self, exporttype: str = "csv", path: str = pwd()) -> None:
        """General purpose Export. Excludes timestamp.

        Args:
            exporttype (str, optional): specify export type. Valid -> ['.csv', '.xlsx']. Defaults to ".csv".
        """
        valid = ['csv', 'xlsx']
        
        if exporttype not in valid:
            raise InvalidExportType(f'{exporttype} is not supported yet.')
        
        with open(jPath(str(Path.home()), '.pastaman', '.m'), 'rb') as m:
            __dat = {
                "target-type":"master",
                "target":"master",
                "username":"master",
                "password":m.read().decode('ascii')
            }
        __data:list[str] = []
        __data.append(__dat)
        __data.extend(self.data)
        
        self.DataFrame = pd.DataFrame(__data).drop('timestamp', axis=1)
        
        if exporttype == 'csv':
            self.DataFrame.to_csv(jPath(path, str(datetime.timestamp(datetime.now())).split('.')[0]+"-pastaman-passwords.csv"), index = False, header = False)
        elif exporttype == 'xlsx':
            self.DataFrame.to_excel(jPath(path, str(datetime.timestamp(datetime.now())).split('.')[0]+"-pastaman-passwords.xlsx"), index=False, header=False)
        
        sys.exit(0)
    
    def importer(self, ext: str, path: str):
        valid = ['.csv', '.xlsx']
        
        if ext not in valid:
            raise InvalidImportType(InvalidImportType.INVALIDIMPORTTYPE, ext)
        
        __newdata = Retransform(path, ext).data
        self.__append(__newdata)
        
        sys.exit(0)