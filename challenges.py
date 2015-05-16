"""Manage the challenges from r/dailyprogrammer
"""
from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime, timedelta
from contextlib import contextmanager
import dateutil.parser


def from_iso(iso_str):
    return dateutil.parser.parse(iso_str)


def to_iso(datetime_obj):
    return datetime_obj.isoformat()


class JSONCredentials(object):
    """Manage the credentials and access token for the Reddit API
    """
    def __init__(self, creds_fname='.credentials.json'):
        self.creds_fname = creds_fname
        with open(creds_fname) as creds_file:
            self._creds_dict = json.load(creds_file)

    def _has_expired(self):
        """Return whether the access token has expired
        """
        expires = self._creds_dict['client_token']['expires']
        if not expires:
            return True
        return from_iso(expires) < datetime.now()

    def _request_token(self):
        """Request an API token

        Token and expiration timestamp are set on success.

        Exception is thrown on failure
        """
        post_params = {'grant_type': 'client_credentials'}
        auth = HTTPBasicAuth(self._creds_dict['client_id'], self._creds_dict['client_secret'])
        access_token_url = 'https://www.reddit.com/api/v1/access_token'
        response = requests.post(access_token_url, auth=auth, params=post_params)
        if response.status_code != 200:
            raise Exception('Error occurred: %s' % response.json())
        # convert to native formats
        token_reponse = response.json()
        expires_in = token_reponse['expires_in']
        expire_time = datetime.now() + timedelta(seconds=expires_in)
        self._creds_dict['client_token']['expires'] = expire_time.isoformat()
        self._creds_dict['client_token']['token'] = token_reponse['access_token']

    def get_token(self):
        """Retrieve a valid API token
        """
        if self._has_expired():
            self._request_token()
            self._dump()
        return self._creds_dict['client_token']['token']

    def _dump(self):
        """Dump credentials back to file
        """
        with open(self.creds_fname, 'w') as creds_file:
            json.dump(self._creds_dict, creds_file, sort_keys=True, indent=4)


@contextmanager
def api_access_token():
    """Yield a valid access token
    """
    yield JSONCredentials().get_token()


def get_challenges():
    """Retrieve the challenges from reddit
    """
    print "Retrieving access token..."
    with api_access_token() as token:
        print "Sending request..."
        headers = {'Authorization': 'bearer ' + token, 'User-Agent': 'DPClient/0.1 by msuozzo'}
        wiki_url = 'https://oauth.reddit.com/r/dailyprogrammer/wiki/challenges'
        wiki_response = requests.get(wiki_url, headers=headers)
    if wiki_response.status_code != 200:
        raise Exception('Error requesting challenges page')
    print "Parsing challenges..."
    html = wiki_response.json()['data']['content_html']
    # ugly hack to load escaped html
    escaped_soup = BeautifulSoup(html)
    soup = BeautifulSoup(escaped_soup.text)
    # table of challenges
    # format: [easy, intermediate, hard, extra]
    challenges = [[], [], [], []]
    challenges_table = soup.tbody
    for ind, cell in enumerate(challenges_table.find_all('td')):
        if cell.a:
            link = cell.a.get('href')
            if link.startswith('/'):
                link = 'http://www.reddit.com' + link
            title = cell.a.get_text(strip=True)
            challenge = (title, link)
            challenges[ind % 4].append(challenge)


def update_challenges():
    pass


if __name__ == '__main__':
    get_challenges()
