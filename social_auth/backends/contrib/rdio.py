from social_auth.utils import dsa_urlopen
from social_auth.backends import ConsumerBasedOAuth, OAuthBackend, BaseOAuth2


class RdioBaseBackend(OAuthBackend):
    def get_user_id(self, details, response):
        return response['key']

    def get_user_details(self, response):
        return {
            'username': response['username'],
            'first_name': response['firstName'],
            'last_name': response['lastName'],
            'fullname': response['displayName'],
        }


class RdioOAuth1Backend(RdioBaseBackend):
    """Rdio OAuth authentication backend"""
    name = 'rdio-oauth1'
    EXTRA_DATA = [
        ('key', 'rdio_id'),
        ('icon', 'rdio_icon_url'),
        ('url', 'rdio_profile_url'),
        ('username', 'rdio_username'),
        ('streamRegion', 'rdio_stream_region'),
    ]

    @classmethod
    def tokens(cls, instance):
        token = super(RdioOAuth1Backend, cls).tokens(instance)
        if token and 'access_token' in token:
            token = dict(tok.split('=')
                            for tok in token['access_token'].split('&'))
        return token


class RdioOAuth2Backend(RdioBaseBackend):
    name = 'rdio-oauth2'
    EXTRA_DATA = [
        ('key', 'rdio_id'),
        ('icon', 'rdio_icon_url'),
        ('url', 'rdio_profile_url'),
        ('username', 'rdio_username'),
        ('streamRegion', 'rdio_stream_region'),
        ('refresh_token', 'refresh_token', True),
        ('token_type', 'token_type', True),
    ]


class RdioOAuth1(ConsumerBasedOAuth):
    AUTH_BACKEND = RdioOAuth1Backend
    REQUEST_TOKEN_URL = 'http://api.rdio.com/oauth/request_token'
    AUTHORIZATION_URL = 'https://www.rdio.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'http://api.rdio.com/oauth/access_token'
    RDIO_API_BASE = 'http://api.rdio.com/1/'
    SETTINGS_KEY_NAME = 'RDIO_OAUTH1_KEY'
    SETTINGS_SECRET_NAME = 'RDIO_OAUTH1_SECRET'

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        try:
            return self.oauth_request(
                access_token,
                self.RDIO_API_BASE,
                data={'method': 'currentUser',
                      'extras': 'username,displayName,streamRegion'},
                method='POST'
            ).json()['result']
        except ValueError:
            return None


class RdioOAuth2(BaseOAuth2):
    AUTH_BACKEND = RdioOAuth2Backend
    AUTHORIZATION_URL = 'https://www.rdio.com/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://www.rdio.com/oauth2/token'
    RDIO_API_BASE = 'https://www.rdio.com/api/1/'
    SETTINGS_KEY_NAME = 'RDIO_OAUTH2_KEY'
    SETTINGS_SECRET_NAME = 'RDIO_OAUTH2_SECRET'
    SCOPE_VAR_NAME = 'RDIO2_PERMISSIONS'
    EXTRA_PARAMS_VAR_NAME = 'RDIO2_EXTRA_PARAMS'

    def user_data(self, access_token, *args, **kwargs):
        try:
            return dsa_urlopen(
                self.RDIO_API_BASE,
                method='POST',
                data={'method': 'currentUser',
                      'extras': 'username,displayName,streamRegion',
                      'access_token': access_token}
            ).json()['result']
        except ValueError:
            return None


# Backend definition
BACKENDS = {
    'rdio-oauth1': RdioOAuth1,
    'rdio-oauth2': RdioOAuth2
}
