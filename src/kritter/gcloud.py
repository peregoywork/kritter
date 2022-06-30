#
# This file is part of Kritter 
#
# All Kritter source code is provided under the terms of the
# GNU General Public License v2 (http://www.gnu.org/licenses/gpl-2.0.html).
# Those wishing to use Kritter source code, software and/or
# technologies under different licensing terms should contact us at
# support@charmedlabs.com. 
#

import os
import time
import pickle 
import requests
import socket
import urllib.request
import google_auth_oauthlib.flow
from google.auth.transport.requests import Request
from .kritter import BASE_DIR
from .kdataclient import KdataClient 
from .gpstoremedia import GPstoreMedia
from .gtextclient import GtextClient
from kritter import Kritter

AUTH_FILE = "gcloud.auth"
SCOPES = {"KstoreMedia": ['https://www.googleapis.com/auth/photoslibrary', 'https://www.googleapis.com/auth/photoslibrary.sharing'], "KtextClient": ['https://mail.google.com/'], "KstoreFile": ['https://www.googleapis.com/auth/drive'], "KtabularClient": ['https://www.googleapis.com/auth/spreadsheets']}
AUTH_SERVER = "https://auth.vizycam.com"

os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = "1"

class Gcloud(KdataClient):

    def __init__(self, etcdir):
        self.flow = None
        self.state = None
        super().__init__([k for k, v in SCOPES.items()])
        self._creds = None
        self.auth_file = os.path.join(etcdir, AUTH_FILE) 


    def available_interfaces(self):
        interfaces = self.interfaces.copy()
        creds = self.creds()
        if creds:
            for i in self.interfaces:
                for s in SCOPES[i]:
                    if s not in creds.scopes:
                        interfaces.remove(i)
                        break 
            return interfaces
        return None

    def get_interface(self, interface):
        if interface in self.available_interfaces():
            if interface=='KstoreMedia':
                return GPstoreMedia(self)
            elif interface=='KtextClient':
                return GtextClient(self)
            else:
                return None

    def _save_creds(self):
        with open(self.auth_file, 'wb') as token:
            pickle.dump(self._creds, token)

    def creds(self):
        if not self.connect():
            return None
        return self._creds  

    def remove_creds(self):
        os.remove(self.auth_file)
        self._creds = None

    def connect(self):
        if self._creds and self._creds.valid:
            return True

        try:
            with open(self.auth_file, 'rb') as token:
                self._creds = pickle.load(token)
        except:
            return False

        if (not self._creds.valid or self._creds.expired) and self._creds.refresh_token:
            try:
                print("Refreshing token...")
                self._creds.refresh(Request())
                self._save_creds()
                print("Success!")
            except Exception as e:
                print("Error refreshing token: ", e)
                return False

        return self._creds.valid

    def get_url(self, client_secret, scopes=SCOPES):
        scopes_list = {i for k, v in scopes.items() for i in v} # set comprehension, no replications

        self.flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            client_secret, scopes=scopes_list, redirect_uri=AUTH_SERVER)
        url, self.state = self.flow.authorization_url(
            # This parameter enables offline access which gives your application
            # an access token and a refresh token for the user's credentials.
            access_type='offline',
            # This parameter enables incremental auth.
            include_granted_scopes='true')

        print("**** url:", url)
        print("**** state:", self.state)
        return url


    def finish_authorization(self):
        if not self.state or not self.flow:
            raise RuntimeError("You need to call get_url() before calling retrieve_code().")
        req = urllib.request.Request(f'{AUTH_SERVER}/poll/?state={self.state}', headers={'User-Agent': 'Mozilla/5.0'})
        try:
            code = urllib.request.urlopen(req, timeout=10).read()
            print("*** received code", code)
            # If we receive b'', it's the same as a timeout (code hasn't arrived) 
            if not code: 
                print("*** no code, sleeping")
                time.sleep(5)
                raise TimeoutError
        except socket.timeout:
            print("*** timeout2")
            raise TimeoutError
        code = code.decode('utf-8')
        self.flow.fetch_token(code=code)                  
        session = self.flow.authorized_session()
        self._creds = session.credentials
        print("*** creds", self._creds, self.flow.credentials)
        self._save_creds()
        return True


