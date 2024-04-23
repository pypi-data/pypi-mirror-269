==============================================
``POST /device/(device_id)/mileage/(mileage)``
==============================================

--------
Synopsis
--------

Set the current mileage of the specified tracker device.


---------------------
Request Header Fields
---------------------

.. include:: /_include/authenticated_session_header_fields.inc


----------------
Request URL Bits
----------------

* ``device_id``: identification of the tracker device to set its
  mileage.

* ``mileage:integer``: new mileage to set for this tracker device as
  the total distance travelled by the vehicle this device is mounted
  on.


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

* ``InvalidAccessException``: if the authenticated user is not the
  owner of this tracker device, nor an administrator of his
  organization, nor an administrator of the platform.

* ``InvalidOperationException``: if the vehicle, which the tracker
  device is mounted on, is moving.

* ``UndefinedObjectException``: if the specified identification
  doesn't refer to any tracker device registered against the platform.
