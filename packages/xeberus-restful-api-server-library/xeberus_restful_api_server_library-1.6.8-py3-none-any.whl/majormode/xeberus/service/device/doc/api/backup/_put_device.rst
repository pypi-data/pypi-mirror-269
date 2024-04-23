======================
``PUT /device/(imei)``
======================

--------
Synopsis
--------

Update one or more properties of the specified device on behalf of the
user that currently owns this device.


---------------------
Request Header Fields
---------------------

.. include:: /_include/authenticated_session_header_fields.inc


----------------
Request URL Bits
----------------

* ``imei``: International Mobile Equipment Identity (IMEI) of the
  device to update some of its properties.


------------------------
Request Query Parameters
------------------------

None.


--------------------
Request Message Body
--------------------

The HTTP request must contain the following JSON structure::

    {
      "is_battery_alarm_muted": boolean,
      "is_device_alarm_muted": boolean,
      "is_security_alarm_muted": boolean,
      "security_level": integer
    }

where:

* ``is_battery_alarm_muted`` (optional): indicate whether the user
  muted the alarm that was triggered when the battery has been
  unplugged or when the level of the battery went down below a
  critical threshold.

* ``is_device_alarm_muted`` (optional): indicate whether the user
  muted the alarm that was triggered when the device is not
  responding anymore.

* ``is_security_alarm_muted`` (optional): indicate whether the user
  muted the alarm system that was triggered when the device has
  detected a movement or a location change while the security level
  is set to ``active``.

* ``security_level`` (optional): indicate the current level of
  security of this device:

  * ``1``: indicate that the alarm system of the device is active,
    which is an alarm that the user manually arms when he leaves his
    vehicle. The user will be urgently alerted of any movement of his
    vehicle.

  * ``0``: indicate that the alarm system of the device is
    passive, which is an alarm that doesn’t need to be manually armed
    when the user leaves his vehicle.  Instead, the alarm  is
    automatically activated when the vehicle doesn't move anymore
    after a few seconds.  The user will be gently notified of any
    movement of his vehicle.


---------------------
Response Message Body
---------------------

The platform returns the following JSON form::

    {
      "imei": string,
      "update_time": timestamp
    }

where:

* ``imei``(required): the International Mobile Equipment Identity
  (IMEI) number of the device which one or more properties have been
  updated.

* ``update_time`` (required): time of the most recent change of one
  or more properties of this device.


----------
Exceptions
----------

The platform MAY raise the following exceptions to indicate that one
or several required conditions have not been respected:

* ``DeletedObjectException``: if the device has been deleted.

* ``DisabledObjectException``: if the device has been disabled.

* ``InvalidOperationException``: if the device is not linked to any
  account or team.

* ``UndefinedObjectException``: if the specified IMEI doesn't
  correspond to any enabled device registered against the platform.
