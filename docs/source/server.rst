Server
========

The server class is used to communicate with the a Jellyfin media server.

Jellyfin Server
----------------

This server requires a running `Jellyfin`_ server with a user defined admin account.
This can be on your local system or a remote server.

The Python `requests`_ library is used in order to facilitate HTTP requests to Jellyfin server. It makes POST requests and passes proper headers, parameters, and payload data.

.. _`requests`: http://docs.python-requests.org/
.. _`jellyfin`: https://github.com/jellyfin/jellyfin