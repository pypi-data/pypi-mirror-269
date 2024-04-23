======================================
``POST /device/(imei)/playback/(slot)``
======================================

--------
Synopsis
--------

Start the playback of a sound effect on the specified device.


---------------------
Request Header Fields
---------------------

.. include:: /_include/authenticated_session_header_fields.inc


----------------
Request URL Bits
----------------

* ``imei``: International Mobile Equipment Identity (IMEI) number of
  the device to start playback.

* ``slot``: the index of the slot of the sound resource to use as
  the datasource.


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

* ``IllegalAccessException``: if the device is not acquired by the
  user on behalf of whom the request is sent.

* ``UndefinedObjectException``: if the specified IMEI doesn't
  correspond to any enabled device registered against the platform.
