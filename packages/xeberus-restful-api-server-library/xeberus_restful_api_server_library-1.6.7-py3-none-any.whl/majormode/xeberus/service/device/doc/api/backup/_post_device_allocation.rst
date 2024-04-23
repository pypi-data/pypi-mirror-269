=========================================
``POST /device/(salted_imei)/allocation``
=========================================

--------
Synopsis
--------

Allocate a registered device to a user account providing this device
is not already acquired by another user.


---------------------
Request Header Fields
---------------------

.. include:: /_include/authenticated_session_header_fields.inc


----------------
Request URL Bits
----------------

* ``imei:string``: International Mobile Equipment Identity (IMEI)
  number of the device to allocate to the user account.


------------------------
Request Query Parameters
------------------------

None.


--------------------
Request Message Body
--------------------

None.


---------------------
Response Message Body
---------------------

None.


----------
Exceptions
----------

The platform MAY raise the following exceptions to indicate that one
or several required conditions have not been respected:

* ``DeletedObjectException``: if the device has been deleted.

* ``DisabledObjectException``: if the device has been disabled.

* ``InvalidOperationException``: if the specified device is already
  acquired by another user account.

* ``MaximumRegisteredDevicesReachedException``: if the maximum
  number of registered devices for the specified user reached and as
  such this user is not allowed not register anymore devices.

* ``UndefinedObjectException``: if the specified IMEI doesn't
  correspond to any enabled device registered against the platform.
