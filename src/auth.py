import httpx
import time

from . import settings

AUTH_ENDPOINT = 'https://meta.wikimedia.org/w/rest.php/oauth2/access_token'

class AuthException(Exception):
    pass

class WikiAuthenticator:
    access_token = None
    expires_at = None # (token creation time) + (expires_in)

    def __auth(self):
        if self.access_token is not None and self.expires_at < time.process_time():
            return
        if len(str(settings.WIKI_ACCESS_TOKEN)) != 0:
            self.access_token = str(settings.WIKI_ACCESS_TOKEN)
            return
        if len(str(settings.WIKI_CLIENT_ID)) == 0 or len(str(settings.WIKI_CLIENT_SECRET)) == 0:
            return
        r = httpx.post(AUTH_ENDPOINT, data={
            'grant_type': 'client_credentials',
            'client_id': settings.WIKI_CLIENT_ID,
            'client_secret': settings.WIKI_CLIENT_SECRET
        })

        if r.status_code == httpx.codes.OK:
            rb = r.json()
            self.access_token = rb['access_token']
            self.expires_at = int(time.process_time() + rb['expires_in'])
        else:
            raise AuthException('Auth Wikimedia Token failed!')

    def token(self):
        if self.access_token is None:
            self.__auth()
        return self.access_token