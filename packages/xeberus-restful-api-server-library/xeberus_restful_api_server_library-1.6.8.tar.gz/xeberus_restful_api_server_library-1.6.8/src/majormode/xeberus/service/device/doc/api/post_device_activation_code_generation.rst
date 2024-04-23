``POST /device/activation/code``
================================

Synopsis
--------

Request a code to activate one or more mobile devices.

The platform may decide to reuse an activation code that has been recently generated for the same individual user or the same organization.  This allows reusing a same code for consecutively activating several mobile devices without having to generate a series of activation codes.


Request Header Fields
---------------------

.. include:: /_include/authenticated_session_header_fields.inc


Request URL Bits
----------------

None.


Request Query Parameters
------------------------

None.


Request Message Body
--------------------

The HTTP request MUST contain the following JSON data::

    {
      "ttl": integer,
      "team_id": string
    }

where:

* ``team_id`` (required): The identification of an organization on behalf of which the activation code is generated.  The authenticated user MUST be an administrator of this organization.

* ``ttl`` (optional): The time-to-live (TTL) in seconds of the activation code before it expires.


Response Message Body
---------------------

The server platform returns the following JSON form::

    {
      "activation_code": string,
      "expiration_time": timestamp
    }

where:

* ``activation_code`` (required): A code that a mobile device needs to scan, for instance as a QR code.  This device will have then to send this code to the server platform in order for the device to be activated.

* ``expiration_time`` (required): The time when this activation code expires.


Exceptions
----------

The platform MAY raise the following exceptions to indicate that one or several required conditions have not been respected:

* ``IllegalAccessException``: If the user on behalf of whom this request is sent is not an administrator of the specified organization.
