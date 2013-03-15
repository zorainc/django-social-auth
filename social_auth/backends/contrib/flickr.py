"""
Flickr OAuth support.

This contribution adds support for Flickr OAuth service. The settings
FLICKR_APP_ID and FLICKR_API_SECRET must be defined with the values
given by Flickr application registration process.

By default account id, username and token expiration time are stored in
extra_data field, check OAuthBackend class for details on how to extend it.
"""
from social_auth.utils import parse_qs
from social_auth.backends import ConsumerBasedOAuth, OAuthBackend


# Flickr configuration
FLICKR_SERVER = 'http://www.flickr.com/services'
FLICKR_REQUEST_TOKEN_URL = '%s/oauth/request_token' % FLICKR_SERVER
FLICKR_AUTHORIZATION_URL = '%s/oauth/authorize' % FLICKR_SERVER
FLICKR_ACCESS_TOKEN_URL = '%s/oauth/access_token' % FLICKR_SERVER


class FlickrBackend(OAuthBackend):
    """Flickr OAuth authentication backend"""
    name = 'flickr'
    # Default extra data to store
    EXTRA_DATA = [
        ('id', 'id'),
        ('username', 'username'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from Flickr account"""
        return {'username': response.get('id'),
                'email': '',
                'first_name': response.get('fullname')}


class FlickrAuth(ConsumerBasedOAuth):
    """Flickr OAuth authentication mechanism"""
    AUTHORIZATION_URL = FLICKR_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = FLICKR_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = FLICKR_ACCESS_TOKEN_URL
    AUTH_BACKEND = FlickrBackend
    SETTINGS_KEY_NAME = 'FLICKR_APP_ID'
    SETTINGS_SECRET_NAME = 'FLICKR_API_SECRET'

    def access_token(self, token):
        """Return request for access token value"""
        # Flickr is a bit different - it passes user information along with
        # the access token, so temporarily store it to view the user_data
        # method easy access later in the flow!
        return parse_qs(self.oauth_request(token,
                                           self.ACCESS_TOKEN_URL).content)

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return {
            'id': access_token['user_nsid'],
            'username': access_token['username'],
            'fullname': access_token['fullname'],
        }

    def auth_extra_arguments(self):
        params = super(FlickrAuth, self).auth_extra_arguments() or {}
        if not 'perms' in params:
            params['perms'] = 'read'
        return params


# Backend definition
BACKENDS = {
    'flickr': FlickrAuth,
}
