"""Emailage api core module."""
import base64
import hmac
import hashlib
import urllib
import logging
import requests

from tools import generate_nonce_timestamp
from tools import split_url_and_query

def get_emailage_url(method, url, consumer_key, consumer_secret):
    """Generate the oauth url for emailAge"""

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

    query_str = query_params + cred_params

    sig_url = method.upper() + "&" + urllib.quote(url, "") + "&" + urllib.quote(query_str, "")

    # Generate the has using customer secret key and create the digest
    hash_result = hmac.new(consumer_secret + "&", sig_url.encode('utf-8'), hashlib.sha1).digest()
    sig = base64.encodestring(hash_result).rstrip()  # Encode string, dropping the leading \n
    oauth_url = url + "?" + query_str + "&oauth_signature=" + urllib.quote(sig.decode(), "")
    return oauth_url




def get_emailage_score(email, customer_key, secret_token, ip=None, use_prod=False):
    """Returns the emailAge score and message.
    :param email: mandatory field
    :param customer_key: as per emailAge api
    :param secret_token: as per emailAge api
    :param ip: optional ip address
    :param use_prod: use emailage production url instead of sandbox
    :return: emailAge Score, Reason message
    """
    if use_prod:
        url = "https://api.emailage.com/EmailAgeValidator/"
    else:
        url = "https://sandbox.emailage.com/EmailAgeValidator/"  # Sandbox

    base_url = url + "?format=json"
    url = get_emailage_url('POST', base_url, customer_key, secret_token)
    data = "{}+{}".format(email, ip) if ip else email
    try:
        r = requests.post(url, data=data)
        resp = eval(r.content)
        logging.info("EmailAge Response: \n {}".format(resp))
        results = resp['query']['results'][0]
    except Exception as e:
        msg = "Something went wrong while getting emailAge score."
        logging.info(msg + " {}: {}.".format(e.__class__, e))
        return False, None, msg
    return True, results['EAScore'], "{}. {}.".format(results.get('EAAdvice'), results.get('EAReason'))
