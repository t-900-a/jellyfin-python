Python Jellyfin module
====================

|travis|_ |coveralls|_


.. |travis| image:: https://travis-ci.org/tiedtoastar/jellyfin-python.svg
.. _travis: https://travis-ci.org/tiedtoastar/jellyfin-python


.. |coveralls| image:: https://coveralls.io/repos/github/tiedtoastar/jellyfin-python/badge.svg
.. _coveralls: https://coveralls.io/github/tiedtoastar/jellyfin-python


A comprehensive Jellyfin module for handling accounts and other future server properties

* release 0.1
* open source: https://github.com/tiedtoastar/jellyfin-python
* Jellyfin is the FREE & OPEN SOURCE media player
* works with Jellyfin 10 and Emby 4.*
* Python 3.x compatible
* comes with documentation

Copyrights
----------

Released under the BSD 3-Clause License. See `LICENSE.txt`_.

Copyright (c) 2019 TiedToAStar <TiedToAStar@protonmail.com>

.. _`LICENSE.txt`: LICENSE.txt

Example Server Configuration
----------
The configurator will look at ./cfg/mediaserver-config.json
The user specified should have admin privileges

.. code-block:: bash

    {
  "host": "127.0.0.1",
  "path": "",
  "port": "8096",
  "protocol": "http",
  "user": "MyEmbyUser" }

Example Project
----------
Check out! https://github.com/tiedtoastar/emby2jellyfin-Migration-Scripts

Want to help?
-------------

If you find this project useful, please consider a donation to the following Monero address:
``47q3TVnd79QcMLqFE2HJC5HTWDadUXtMDVavERPfeT3xFiBeqQQX6knBNALTz4aciC6pSbnLoMCHXXsQDCPV1BT7TqoqZxW``


Development
-----------

1. Clone the repo
2. Create virtualenv & activate it

.. code-block:: bash

    python3 -m venv .venv
    source .venv/bin/activate

3. Install dependencies

.. code-block:: bash

    pip install -r requirements.txt -r test_requirements.txt

4. Do your thing

5. Run tests

.. code-block:: bash

    pytest
