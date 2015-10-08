#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Nose tests for emailAge API functions"""

import requests
from emailage import api as oauth
import logging
import unittest


class TestEmailageAPI(unittest.TestCase):
    """Test the emailAge API"""

    def setUp(self):
        logging.debug('setting up...')
        self.account_sid, self.auth_token = raw_input("Enter your Customer SSID: "), \
                                            raw_input("Enter your Auth Token: "),
        self.query = "wang@emailage.com+142.136.211.118"  # The email or IP you want verify
        self.result_format = "json"  # XML or JSON
        self.base_url = "https://sandbox.emailage.com/EmailAgeValidator/"

    def tearDown(self):
        logging.debug('tearing down...')

    # POST i.e. https://sandbox.emailage.com/EmailAgeValidator/?format=json  + body
    def test_post(self):
        orig_url = self.base_url + "?format=" + self.result_format
        url = oauth.get_emailage_url("POST", orig_url, self.account_sid, self.auth_token)
        data = self.query
        req = requests.post(url, data=data)
        resp = eval(req.content)
        assert resp['query']['results'][0]['EAScore'], "EA Score not found."

    # GET i.e
    # https://sandbox.emailage.com/EmailAgeValidator/?format=json&query=wang@emailage.com+142.136.211.118&user_email=
    def test_get(self):
        orig_url = self.base_url + "?format=" + self.result_format + "&query=" + self.query + "&user_email="
        url = oauth.get_emailage_url("GET", orig_url, self.account_sid, self.auth_token)
        req = requests.get(url)
        resp = eval(req.content)
        assert resp['query']['results'][0]['EAScore'], "EA Score not found."

    def test_get_score(self):
        score = oauth.get_emailage_score('me@tester.com', self.account_sid, self.auth_token, '127.0.0.1')
        assert score, "No score returned."

