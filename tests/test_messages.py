#!/usr/bin/env python
"""Nose tests for emailAge API messages"""

import logging
import sys

sys.path.insert(0, '..')

import unittest

from emailage import api as oauth
from emailage.exceptions import EmailAgeServiceException


class TestEmailageMessages(unittest.TestCase):
    """Test the emailAge API messages/errors handling."""

    def setUp(self):
        logging.debug('setting up...')
        self.query_email = 'wang@emailage.com'
        self.query_ip = '142.136.211.118'

    def tearDown(self):
        logging.debug('tearing down...')

    # Test authentication error and missing credentials messages
    def test_no_creds_message(self):
        with self.assertRaises(EmailAgeServiceException) as ctx_mgr:
            _, _ = oauth.get_emailage_score(email=self.query_email, ip=self.query_ip,
                                            customer_key='',
                                            secret_token='', use_prod=False,
                                            score_only=True)

        assert 'Missing Credentials' in str(ctx_mgr.exception)

        with self.assertRaises(EmailAgeServiceException) as ctx_mgr:
            _, _ = oauth.get_emailage_score(email=self.query_email, ip=self.query_ip,
                                            customer_key='invalid',
                                            secret_token='credentials', use_prod=False,
                                            score_only=True)

            assert 'Authentication Error' in str(ctx_mgr.exception)


if __name__ == "__main__":
    unittest.main()
