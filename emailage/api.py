# coding=utf-8
"""emailAge core API module.

This module contains all methods that are required to make a request
fromt the emailAge API.
"""
from __future__ import unicode_literals

import hmac
import hashlib
import logging
from ast import literal_eval  # import json

# Safe way to import url quote for py2 and py3
# http://docs.pythonsprints.com/python3_porting/py-porting.html
try:
    from urllib import quote as urllib_quote
    from urllib import urlencode as urllib_urlencode
    from base64 import encodestring as base64_encodebytes
except ImportError:
    from urllib.parse import quote as urllib_quote
    from urllib.parse import urlencode as urllib_urlencode
    from base64 import encodebytes as base64_encodebytes
import requests

from .tools import generate_nonce_timestamp
from .tools import split_url_and_query
from .exceptions import EmailAgeServiceException

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
    query_params = urllib_quote(orig_query, safe='=&') + '&'

    # URL encode credential params
    cred_params = urllib_urlencode({'oauth_consumer_key': consumer_key, 'oauth_nonce': nonce,
                                    'oauth_signature_method': 'HMAC-SHA1', 'oauth_timestamp': timestamp,
                                    'oauth_version': '1.0'})
    """ivar: credential parameters required in the payload."""

    query_str = query_params + cred_params

    sig_url = method.upper() + "&" + urllib_quote(url, "") + "&" + urllib_quote(query_str, "")

    # Generate the has using customer secret key and create the digest
    to_hash = "{}&".format(consumer_secret)
    hash_result = hmac.new(to_hash.encode('utf-8'), sig_url.encode('utf-8'), digestmod=hashlib.sha1).digest()
    # py2 style
    # hash_result = hmac.new(str(to_hash), sig_url, digestmod=hashlib.sha1).digest()
    sig = base64_encodebytes(hash_result).rstrip()  # Encode string, dropping the leading
    """ivar: signature based on consumer secret to validate request."""

    oauth_url = url + "?" + query_str + "&oauth_signature=" + urllib_quote(sig.decode(), "")
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
    :param score_only: only return score instead of entire payload.
    """

    if not customer_key or not secret_token:
        raise EmailAgeServiceException(error_code=None,
                                       value="Missing Credentials: Customer key and/or secret token not supplied.")

    base_url = get_base_url(use_prod) + "?format=json"
    url = get_emailage_url('POST', base_url, customer_key, secret_token)
    data = "{}+{}".format(email, ip) if ip else email
    """ivar: payload sent to emailAge. Email and optionally includes IP."""

    logger.info("EmailAge Request: {} {}".format(url, data))
    r = requests.post(url, data=data)
    resp = literal_eval(r.content.decode('utf-8-sig'))  # json.loads now working.
    # import json; resp = json.loads(str(r.content.decode('utf-8-sig')))  # json.loads now working.
    logger.info("EmailAge Response: {}".format(resp))
    response_status = resp['responseStatus']
    if response_status.get('status') == 'failed':
        raise EmailAgeServiceException(error_code=response_status.get('errorCode'),
                                       value=response_status.get('description'))
    try:
        results = resp['query']['results'][0]
    except IndexError:
        logger.info("EmailAge Response: None due to error.")
        raise EmailAgeServiceException(error_code=None,
                                       value="Could not get emailAge score. {}".format(resp))

    if score_only:
        return results['EAScore'], "{}. {}.".format(results.get('EAAdvice'), results.get('EAReason'))
    else:
        return results, ""
