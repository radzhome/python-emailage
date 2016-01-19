"""Emailage api tools module."""
import uuid


def generate_nonce_timestamp():
    """Generate pseudo-random number and seconds since epoch (UTC)."""
    nonce = uuid.uuid1()
    oauth_timestamp, oauth_nonce = str(nonce.time), nonce.hex
    return oauth_nonce, oauth_timestamp


def split_url_and_query(url):
    """Split the query from the url"""
    try:
        index = url.index('?')
    except ValueError:
        return url, ""
    query = url[index + 1:]
    url = url[:index]
    return url, query
