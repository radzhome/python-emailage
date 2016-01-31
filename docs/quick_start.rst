.. _quick_start:

.. include:: global.txt

Quick Start
===========

To get you started, a comprehensive set of is included in tests.

Get entire response
-------------------

.. code-block:: python

    score, message = oauth.get_emailage_score(email=<email>, ip=<remote_ip>,
                                              customer_key=<account_sid>,
                                              secret_token=<auth_token>, use_prod=True,
                                              score_only=True)
    print score

Get score and message only
--------------------------

.. code-block:: python

    score, message = oauth.get_emailage_score(email=<email>, ip=<remote_ip>,
                                              customer_key=<account_sid>,
                                              secret_token=<auth_token>, use_prod=True,
                                              score_only=True)
    print score
