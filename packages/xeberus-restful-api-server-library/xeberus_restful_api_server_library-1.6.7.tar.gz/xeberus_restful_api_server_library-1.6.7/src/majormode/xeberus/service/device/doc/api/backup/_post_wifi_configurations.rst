==============
``POST /wifi``
==============

--------
Synopsis
--------

Define the security configuration of a list of Wi-Fi networks that
will be shared with the devices of the authenticated users or an
organisation this user belongs to.


---------------------
Request Header Fields
---------------------

.. include:: /_include/authenticated_session_header_fields.inc


----------------
Request URL Bits
----------------

None.

------------------------
Request Query Parameters
------------------------

* ``team_id:string`` (optional): identification of an organisation this
  user belongs to.


--------------------
Request Message Body
--------------------

The HTTP request must contain the following JSON structure that
declares the set of variables that describe Wi-Fi configuration::

    [
      {
        "bssid": string,
        "password": string,
        "ssid": string,
      },
      ...
    ]

where:

* ``bssid`` (optional): Basic Service Set Identifier (BSSID) that
  uniquely identifies a Wi-Fi hotspot.

* ``password`` (required): hashed version of the password to connect
  to the Wi-Fi hotspot, also known as the prre-shared key for use with
  WPA-PSK.

* ``ssid`` (required): Service Set Identifier (SSID), which is a
  friendly name that identifies the Wi-Fi hotspot.


---------------------
Response Message Body
---------------------

None.


----------
Exceptions
----------

None.
