"""
Tumblr OAuth 1.0a support.

Take a look to http://www.tumblr.com/docs/en/api/v2

You need to register OAuth site here:
http://www.tumblr.com/oauth/apps

Then update your settings values using registration information

ref:
https://github.com/gkmngrgn/django-tumblr-auth
"""
from social_auth.utils import parse_qs
from social_auth.backends import ConsumerBasedOAuth, OAuthBackend


TUMBLR_SERVER = 'www.tumblr.com'
TUMBLR_AUTHORIZATION_URL = 'http://%s/oauth/authorize' % TUMBLR_SERVER
TUMBLR_REQUEST_TOKEN_URL = 'http://%s/oauth/request_token' % TUMBLR_SERVER
TUMBLR_ACCESS_TOKEN_URL = 'http://%s/oauth/access_token' % TUMBLR_SERVER
TUMBLR_CHECK_AUTH = 'http://api.tumblr.com/v2/user/info'


class TumblrBackend(OAuthBackend):
    name = 'tumblr'

    def get_user_id(self, details, response):
        return details['username']

    def get_user_details(self, response):
        # http://www.tumblr.com/docs/en/api/v2#user-methods
        user_info = response['response']['user']
        data = {'username': user_info['name']}
        blogs = user_info['blogs']
        for blog in blogs:
            if blog['primary']:
                data['fullname'] = blog['title']
                break
        return data

    @classmethod
    def tokens(cls, instance):
        """
        Return the tokens needed to authenticate the access to any API the
        service might provide. Tumblr uses a pair of OAuthToken consisting
        on a oauth_token and oauth_token_secret.

        instance must be a UserSocialAuth instance.
        """
        token = super(TumblrBackend, cls).tokens(instance)
        if token and 'access_token' in token:
            token = dict(tok.split('=')
                            for tok in token['access_token'].split('&'))
        return token


class TumblrAuth(ConsumerBasedOAuth):
    AUTH_BACKEND = TumblrBackend
    AUTHORIZATION_URL = TUMBLR_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = TUMBLR_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = TUMBLR_ACCESS_TOKEN_URL
    SERVER_URL = TUMBLR_SERVER
    SETTINGS_KEY_NAME = 'TUMBLR_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'TUMBLR_CONSUMER_SECRET'

    def user_data(self, access_token):
        try:
            return self.oauth_request(access_token, TUMBLR_CHECK_AUTH).json()
        except ValueError:
            return None

    def unauthorized_token(self):
        return parse_qs(self.oauth_request(
            token=None,
            url=self.REQUEST_TOKEN_URL
        ).content)


BACKENDS = {
    'tumblr': TumblrAuth
}
