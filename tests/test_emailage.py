#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Nose tests for emailAge API functions"""

from ast import literal_eval
import logging
import re
import sys

sys.path.insert(0, '..')

import requests
import unittest

from emailage import api as oauth
from config import ACCOUNT_SSID
from config import AUTH_TOKEN
from config import USE_PROD


@unittest.skipIf(not ACCOUNT_SSID, "No credentials provided.")
class TestEmailageAPI(unittest.TestCase):
    """Test the emailAge API"""

    def setUp(self):
        logging.debug('setting up...')

        # Replace credentials here.
        self.account_sid = ACCOUNT_SSID
        self.auth_token = AUTH_TOKEN
        self.query_email = 'wang@emailage.com'
        self.query_ip = '142.136.211.118'
        self.query = "{}+{}".format(self.query_email, self.query_ip)  # The email or IP you want verify
        self.result_format = "json"  # XML or JSON
        self.base_url = oauth.get_base_url(use_prod=USE_PROD)

    def tearDown(self):
        logging.debug('tearing down...')

    # POST i.e.
    # https://sandbox.emailage.com/EmailAgeValidator/?format=json  + body
    def test_post(self):
        orig_url = self.base_url + "?format=" + self.result_format
        url = oauth.get_emailage_url("POST", orig_url, self.account_sid, self.auth_token)
        data = self.query
        req = requests.post(url, data=data)
        resp = literal_eval(req.content.decode('utf-8-sig'))
        assert resp['query']['results'][0]['EAScore'], "EA Score not found. {}".format(resp)

    # POST with xml output
    def test_post_xml(self):
        orig_url = self.base_url + "?format=xml"
        url = oauth.get_emailage_url("POST", orig_url, self.account_sid, self.auth_token)
        data = self.query
        req = requests.post(url, data=data)
        rex = re.compile(r'<EAScore>(.*?)</EAScore>')
        match = rex.search(req.content.decode('utf-8-sig'))
        assert match.groups()[0].strip(), req.content

    # GET i.e
    # https://sandbox.emailage.com/EmailAgeValidator/?format=json&query=wang@emailage.com+142.136.211.118&user_email=
    def test_get(self):
        orig_url = self.base_url + "?format=" + self.result_format + "&query=" + self.query + "&user_email="
        url = oauth.get_emailage_url("GET", orig_url, self.account_sid, self.auth_token)
        req = requests.get(url)
        resp = literal_eval(req.content.decode('utf-8-sig'))
        logging.debug(resp)
        assert resp['query']['results'][0]['EAScore'], "EA Score not found."

    # Test full result and score alone.
    def test_get_score(self):
        score, message = oauth.get_emailage_score(email=self.query_email, ip=self.query_ip,
                                                  customer_key=self.account_sid,
                                                  secret_token=self.auth_token, use_prod=USE_PROD,
                                                  score_only=True)
        assert score, "No score returned {}.".format(message)

        score, message = oauth.get_emailage_score(email=self.query_email, ip=self.query_ip,
                                                  customer_key=self.account_sid,
                                                  secret_token=self.auth_token, use_prod=USE_PROD,
                                                  score_only=False)
        assert score, "No score returned. {}.".format(message)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    unittest.main()
