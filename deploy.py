import requests
import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

class Synology:
    def __init__(self, scheme, host, port):
        self.scheme = scheme
        self.host = host
        self.port = port

        self.baseUrl = '{}://{}:{}/webapi/'.format(scheme, host, port)
        self.defaultCookies = {}

    def login(self, username: str, password: str) -> None:
        res = requests.get(self.baseUrl + 'auth.cgi', {
            'api': 'SYNO.API.Auth',
            'version' : '3',
            'method': 'login',
            'account': username,
            'passwd': password,
            'session': 'yolo',
            'format': 'sid'
        })
        json = res.json()

        if not json['success']:
            raise Exception('Login failed!')

        self.sid = json['data']['sid']
        self.defaultCookies['id'] = self.sid

    def logout(self) -> None:
        res = requests.get(self.baseUrl + 'auth.cgi', {
            'api': 'SYNO.API.Auth',
            'version' : '3',
            'method': 'logout',
        })
        json = res.json()

        if not json['success']:
            raise Exception('Logout failed!')

        self.sid = None
        self.defaultCookies['id'] = None

    def getDefaultCert(self) -> dict:
        res = requests.get(self.baseUrl + 'entry.cgi',
            params = {
                'api': 'SYNO.Core.Certificate.CRT',
                'version': 1,
                'method': 'list'
            },
            cookies = self.defaultCookies
        )
        json = res.json()

        if not json['success']:
            raise Exception('Could not get default certificate')

        for certificate in json['data']['certificates']:
            if certificate['is_default']:
                return certificate

    def importDefaultCert(self, desc: str, cert: str, chain: str, key: str) -> str:
        res = requests.post(self.baseUrl + 'entry.cgi',
            params = {
                'api': 'SYNO.Core.Certificate',
                'version' : '1',
                'method': 'import',
            },
            files = [
                ('key', (os.path.basename(key), open(key, 'rb'), 'application/octet-stream')),
                ('cert', (os.path.basename(cert), open(cert, 'rb'), 'application/octet-stream')),
                ('inter_cert', (os.path.basename(chain), open(chain, 'rb'), 'application/octet-stream')),
                ('desc', (None, desc)),
                ('id', (None, '')),
                ('as_default', (None, 'True'))
            ],
            cookies = self.defaultCookies
        )
        json = res.json()

        if not json['success']:
            raise Exception('Could not import certifcate')

        return json['data']['id']

    def deleteCert(self, id: str) -> dict:
        res = requests.post(self.baseUrl + 'entry.cgi',
            data = {
                'api': 'SYNO.Core.Certificate.CRT',
                'version': 1,
                'method': 'delete',
                'ids': json.dumps([id])
            },
            cookies = self.defaultCookies
        )
        body = res.json()

        if not body['success']:
            raise Exception('Could not delete certificate')

        return body['data']

load_dotenv()

synoScheme = os.getenv('SYNO_SCHEME', 'https')
synoHost = os.getenv('SYNO_HOST', None)
synoPort = os.getenv('SYNO_PORT', 5001)
synoUsername = os.getenv('SYNO_USERNAME', None)
synoPassword = os.getenv('SYNO_PASSWORD', None)

if synoHost == None: raise Exception('Variable SYNO_HOST is not defined!')
if synoUsername == None: raise Exception('Variable SYNO_USERNAME is not defined!')
if synoPassword == None: raise Exception('Variable SYNO_PASSWORD is not defined!')

keyFile = os.getenv('KEY_FILE', None)
certFile = os.getenv('CERT_FILE', None)
chainFile = os.getenv('CHAIN_FILE', None)

if keyFile == None: raise Exception('Variable KEY_FILE is not defined!')
if certFile == None: raise Exception('Variable CERT_FILE is not defined!')
if chainFile == None: raise Exception('Variable CHAIN_FILE is not defined!')

syno = Synology(synoScheme, synoHost, synoPort)

print('Connecting with {} to {}://{}:{}'.format(synoUsername, synoScheme, synoHost, synoPort))
syno.login(synoUsername, synoPassword)
print('Logged in. SID: ' + syno.sid)

oldCert = syno.getDefaultCert()
print('Current default certificate: [{}] ({})'.format(oldCert['id'], oldCert['subject']['common_name']))

desc = 'Imported: {}'.format(datetime.now().replace(microsecond=0).isoformat())
newCertId = syno.importDefaultCert(desc, certFile, chainFile, keyFile)
print('Imported new certificate [{}]'.format(newCertId))

print('Deleting previous default certificate [{}] (may take a while)..'.format(oldCert['id']))
deleteInfo = syno.deleteCert(oldCert['id'])
message = 'Deleted certificate [{}].'.format(oldCert['id'])
if deleteInfo['restart_httpd']:
    message += ' Restarting webserver..'
print(message)

syno.logout()
print('Logged out.')
