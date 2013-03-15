import six

if six.PY3:
    from urllib.request import Request, build_opener, HTTPCookieProcessor, \
                               HTTPRedirectHandler
    from http.cookiejar import CookieJar
else:
    from urllib2 import Request, build_opener, HTTPCookieProcessor, \
                        HTTPRedirectHandler
    from cookielib import CookieJar
