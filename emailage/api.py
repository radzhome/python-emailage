"""emailAge core API module.

This module contains all methods that are required to make a request
fromt the emailAge API.
"""
import base64
import hmac
import hashlib
import urllib
import logging
from ast import literal_eval

import requests

from tools import generate_nonce_timestamp
from tools import split_url_and_query

logger = logging.getLogger('emailage')


def get_emailage_url(method, url, consumer_key, consumer_secret):
    """Generate the oauth url for emailAge
    @param method: can be POST or GET.
    @param url: base url to use, either prod or sandbox..
    @param consumer_key: consumer key credential for authentication.
    @param consumer_secret: consumer secret credential for authentication.
    """

    if not method:
        method = "GET"

    nonce, timestamp = generate_nonce_timestamp()
    url, orig_query = split_url_and_query(url)

    # URL parse the query, with equal and and chars as safe
    query_params = urllib.quote(orig_query, safe='=&') + '&'

    # URL encode credential params
    cred_params = urllib.urlencode({'oauth_consumer_key': consumer_key, 'oauth_nonce': nonce,
                                    'oauth_signature_method': 'HMAC-SHA1', 'oauth_timestamp': timestamp,
                                    'oauth_version': '1.0'})
    """ivar: credential parameters required in the payload."""

    query_str = query_params + cred_params

    sig_url = method.upper() + "&" + urllib.quote(url, "") + "&" + urllib.quote(query_str, "")

    # Generate the has using customer secret key and create the digest
    hash_result = hmac.new(consumer_secret + "&", sig_url.encode('utf-8'), hashlib.sha1).digest()
    sig = base64.encodestring(hash_result).rstrip()  # Encode string, dropping the leading
    """ivar: signature based on consumer secret to validate request."""

    oauth_url = url + "?" + query_str + "&oauth_signature=" + urllib.quote(sig.decode(), "")
    return oauth_url


def get_base_url(use_prod=False):
    """Returns the base url, either sandbox or prod.
    @param use_prod: use production url or sandbox.
    """
    if use_prod:
        service_url = "https://api.emailage.com/EmailAgeValidator/"
    else:
        service_url = "https://sandbox.emailage.com/EmailAgeValidator/"  # Sandbox
    return service_url


def get_emailage_score(email, customer_key, secret_token, ip=None, use_prod=False, score_only=True):
    """Returns the emailAge score and message.
    @param email: email address to query for, mandatory field.
    @param customer_key: customer key as per emailAge api.
    @param secret_token: secret key as per emailAge api.
    @param ip: optional ip address to include in the query.
    @param use_prod: use emailage production url instead of sandbox.
    @return: success, emailAge score data, message
    """

    base_url = get_base_url(use_prod) + "?format=json"
    url = get_emailage_url('POST', base_url, customer_key, secret_token)
    data = "{}+{}".format(email, ip) if ip else email
    """ivar: payload sent to emailAge. Email and optionally includes IP."""

    try:
        logger.info("EmailAge Request: {} {}".format(url, data))
        r = requests.post(url, data=data)
        resp = literal_eval(r.content)
        logger.info("EmailAge Response: {}".format(resp))
        results = resp['query']['results'][0]
    except Exception as e:
        msg = "Could not get emailAge score. {}: {}.".format(e.__class__, e)
        logger.info("EmailAge Response: None due to error.")
        return False, None, msg

    if score_only:
        return True, results['EAScore'], "{}. {}.".format(results.get('EAAdvice'), results.get('EAReason'))
    else:
        return True, results, ""