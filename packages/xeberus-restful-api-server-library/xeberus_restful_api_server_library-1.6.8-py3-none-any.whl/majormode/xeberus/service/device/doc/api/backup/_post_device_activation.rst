==================================
``POST /device/(imei)/activation``
==================================

--------
Synopsis
--------

Activate a device which registration is pending.


---------------------
Request Header Fields
---------------------

.. include:: /_include/authenticated_session_header_fields.inc


----------------
Request URL Bits
----------------

* ``imei``: International Mobile Equipment Identity (IMEI) number of
  the device to activate and to allocate to a given user account.


------------------------
Request Query Parameters
------------------------

None.


--------------------
Request Message Body
--------------------

The HTTP request must contains the following JSON structure::

   {
     "account_id": string,
     "team_id": string
   }

where:

* ``account_id`` (required): identification of the account of the
  user that is allocated this device.

* ``team_id`` (optional): identification of a team that is allocated
  this device.  The specified user account MUST belong to this team.

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

* ``IllegalAccessException``: if the user account on behalf of this
  request is sent is not an administrator of the Xeberus team.

* ``InvalidOperationException``: if the specified device is already
  activated.

* ``UndefinedObjectException``: if the specified IMEI doesn't
  correspond to any device registered against the platform.
