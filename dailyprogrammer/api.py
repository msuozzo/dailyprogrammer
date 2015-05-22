"""Provide an interface with the reddit API
"""
import json
from datetime import datetime, timedelta

import requests
from requests.auth import HTTPBasicAuth
import dateutil.parser


class AbstractCredentialManager(object):
    """Absctract class for CredentialManagers, responsible for managing API
    access credentials.
    """
    def get_api_creds(self):
        """Return a 2-tuple of (client_id, client_secret)
        """
        raise NotImplementedError()

    def get_token(self):
        """Return a 2-tuple of (access_token, access_token_expires) where
        access_token_expires is a datetime object representing the time at
        which the access_token will become invalid.
        """
        raise NotImplementedError()

    def put_token(self, token_str, expire_datetime):
        """Store a new access token and token expire time.
        """
        raise NotImplementedError()


class JSONCredentialManager(AbstractCredentialManager):
    """Manage API credentials using a JSON file as backing.
    """
    def __init__(self, creds_fname='.credentials.json'):
        self.creds_fname = creds_fname
        with open(creds_fname) as creds_file:
            self._creds_dict = json.load(creds_file)

    def get_api_creds(self):
        return self._creds_dict['client_id'], self._creds_dict['client_secret']

    def get_token(self):
        token = self._creds_dict['client_token']
        expire_datetime = JSONCredentialManager._from_iso(token['expires'])
        return token['token'], expire_datetime

    def put_token(self, token_str, expire_datetime):
        self._creds_dict['client_token']['token'] = token_str
        expire_iso = JSONCredentialManager._to_iso(expire_datetime)
        self._creds_dict['client_token']['expires'] = expire_iso
        self._dump()

    def _dump(self):
        """Dump credentials back to file
        """
        with open(self.creds_fname, 'w') as creds_file:
            json.dump(self._creds_dict, creds_file, sort_keys=True, indent=4)

    @staticmethod
    def _from_iso(iso_str):
        """Converts an ISO 8601 time string to a datetime object
        """
        return dateutil.parser.parse(iso_str)

    @staticmethod
    def _to_iso(datetime_obj):
        """Converts a datetime object to a ISO 8601 time string
        """
        return datetime_obj.isoformat()


class RedditAPIAdapter(object):
    """Manage the credentials and access token for the Reddit API
    """
    def __init__(self, manager=None):
        self.manager = JSONCredentialManager() if manager is None else manager

    def _request_token(self):
        """Request an access token from the reddit API

        Token and expiration timestamp are set on success.

        Exception is thrown on failure.
        """
        post_params = {'grant_type': 'client_credentials'}
        id_, secret = self.manager.get_api_creds()
        auth = HTTPBasicAuth(id_, secret)
        access_token_url = 'https://www.reddit.com/api/v1/access_token'
        response = requests.post(access_token_url, auth=auth, params=post_params)
        if response.status_code != 200:
            raise Exception('Error occurred: %s' % response.json())
        token_reponse = response.json()
        # number of seconds the token will be valid for
        lease_duration = token_reponse['expires_in']
        expire_time = datetime.now() + timedelta(seconds=lease_duration)
        self.manager.put_token(token_reponse['access_token'], expire_time)

    def get_token(self):
        """Retrieve a valid API token
        """
        token, expires = self.manager.get_token()
        if expires < datetime.now():
            self._request_token()
            token, expires = self.manager.get_token()
        return token
