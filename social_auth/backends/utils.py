from requests_oauthlib import OAuth1
from oauthlib.oauth1 import SIGNATURE_TYPE_AUTH_HEADER

from social_auth.models import UserSocialAuth
from social_auth.utils import dsa_urlopen


def consumer_oauth_url_request(backend, url, user_or_id, redirect_uri='/',
                               json=True):
    """Builds and retrieves an OAuth signed response."""
    user = UserSocialAuth.resolve_user_or_id(user_or_id)
    oauth_info = user.social_auth.filter(provider=backend.AUTH_BACKEND.name)[0]
    response = build_consumer_oauth_request(backend, oauth_info.tokens, url,
                                            redirect_uri)
    return response.json() if json else response.content


def build_consumer_oauth_request(backend, token, url, redirect_uri='/',
                                 oauth_verifier=None, extra_params=None,
                                 data=None, method='GET',
                                 signature_type=SIGNATURE_TYPE_AUTH_HEADER):
    """Builds a Consumer OAuth request."""
    key, secret = backend.get_key_and_secret()
    token = token or {}
    oauth = OAuth1(key, secret,
                   resource_owner_key=token.get('oauth_token'),
                   resource_owner_secret=token.get('oauth_token_secret'),
                   callback_uri=redirect_uri,
                   verifier=oauth_verifier,
                   signature_type=signature_type)
    return dsa_urlopen(url, method=method, params=extra_params, data=data,
                       auth=oauth)
