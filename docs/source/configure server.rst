Configuring the server
=======================

This python module reads and write to a file containing the server configuration.

Instantiate this configuration object within your project. When the file is not found, input will be requested.

.. code-block:: python

    from configurator.mediaserver import mediaServer_config

    def sourceMediaServer():
    myconfig = mediaServer_config()

    try:
        mediaserver = MediaServer(myconfig)
        return mediaserver
    except Exception as inst:
        return inst

The configuration object contains the following attributes:

protocol, host, port, path, user, password

The password is NOT stored in the configuration file and will be requested every time that the object is instantiated.
