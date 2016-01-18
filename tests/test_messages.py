#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Nose tests for emailAge API functions"""

from ast import literal_eval
import logging
import re
import sys

sys.path.insert(0, '..')

import unittest

from emailage import api as oauth


class TestEmailageErrors(unittest.TestCase):
    """Test the emailAge API"""

    def setUp(self):
        logging.debug('setting up...')
        self.query_email = 'wang@emailage.com'
        self.query_ip = '142.136.211.118'

    def tearDown(self):
        logging.debug('tearing down...')

    # Test full result and score alone.
    def test_no_creds_message(self):
        success, score, message = oauth.get_emailage_score(email=self.query_email, ip=self.query_ip,
                                                           customer_key='',
                                                           secret_token='', use_prod=False,
                                                           score_only=True)
        # assert score, "No score returned {}.".format(message)


if __name__ == "__main__":
    unittest.main()
