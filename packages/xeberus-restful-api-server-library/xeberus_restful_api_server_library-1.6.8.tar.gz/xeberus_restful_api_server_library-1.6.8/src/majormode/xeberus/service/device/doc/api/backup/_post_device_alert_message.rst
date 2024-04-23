==========================================
``POST /device/(device_id)/alert_message``
==========================================

--------
Synopsis
--------

Notify the platform from one or more alerts that the device has
detected.

An alert starts whenever the device detects a movement based on the
values read from a built-in motion sensor, such as a gyroscope or an
accelerometer.  An alert stops when no movement is detected after a
few seconds.

Depending on the current alert mode of the device, an alert event is
considered either as a serious threat (active mode), either as
expected (passive mode).

While active mode engaged, an alarm has to be immediately raised to
the owner of the device.  While passive mode enabled, a simple
notification is sent to the owner of the device.


---------------------
Request Header Fields
---------------------

.. include:: /_include/anonymous_session_header_fields.inc


----------------
Request URL Bits
----------------

* ``device_id``: identification of the device that sends this alert
  message.


------------------------
Request Query Parameters
------------------------

* ``s`` (required): a seed, which is a "number used once" (nonce) --
  also known as pseudo-random number -- encrypted with keys shared with
  the platform.  This seed is used to verify the authentication of the
  device in order to prevent spoofing attack.  For further information
  about how to generate this seed, please contact the server platform
  development team.


--------------------
Request Message Body
--------------------

The HTTP request must contains the following JSON structure::

    [
      {
        "alert_id": string,
        "event_time": timestamp,
        "event_type": string,
        "location": {
          "accuracy": decimal,
          "altitude": decimal,
          "bearing": decimal,
          "fix_time": timestamp,
          "latitude": decimal,
          "longitude": decimal,
          "provider": string,
          "speed": decimal
        },
        "sensor_values": [ decimal, decimal, decimal ],
      },
      ...
    ]

where:

* ``alert_id`` (required): identification of the alert which is unique
  whether the alert starts or it stops.

* ``event_time`` (required): time when the device raises this alert
  event, i.e., when the alert started or when it stopped.  This time
  could be slightly different from the time when the device sent this
  alert to the platform, for instance, in case of limited network
  connectivity, the device decided to cache locally this alert before
  sending it eventually to the platform.

* ``event_type`` (required): indicate if the alert started or
  stopped:

  * ``alert_start``: the device has detected a significant movement of the
    vehicle which the device is mounted on.

  * ``alert_stop``: the device has not dectected any movement after a few
    seconds.

* ``location`` (optional): last known location of the device when this
  event occurred:

  * ``accuracy`` (required): accuracy in meters of the location.

  * ``altitude`` (required): altitude in meters of the location.

  * ``bearing`` (optional): bearing in degrees.  Bearing is the horizontal
    direction of travel of the device, and is not related to the device
    orientation.  It is guaranteed to be in the range ``[0.0, 360.0]``.

  * ``fix_time`` (required): time when the device determined the
    information of this fix.

  * ``latitude`` (required): latitude-angular distance, expressed in
    decimal degrees (WGS84 datum), measured from the center of the Earth,
    of a point north or south of the Equator corresponding to the
    location.

  * ``longitude`` (required): longitude-angular distance, expressed in
    decimal degrees (WGS84 datum), measured from the center of the Earth,
    of a point east or west of the Prime Meridian corresponding to the
    location.

  * ``provider`` (required): code name of the location provider that
    reported the location.

    * ``gps``: indicate that the location has been provided by a Global
      Positioning System (GPS).

    * ``network``: indicate that the location has been provided by an hybrid
      positioning system, which uses different positioning technologies,
      such as Global Positioning System (GPS), Wi-Fi hotspots, cell tower
      signals.

  * ``speed`` (optional): speed in meters/second over the ground.

* ``sensor_values`` (optional): acceleration minus Gx on the 3 axes if
  the motion sensor used on the device is an accelerometer, or the
  angular speed around the 3 axes in radians/second if the motion
  sensor used is a gyroscope.  The value of an event is used as
  debugging information.


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

* ``IllegalAccessException``: if the given seed has not been
  successfully verified, meaning that someone or a program tries to
  masquerade as the specified device (spoofing attack).

* ``InvalidOperationException``: if the device has not been activated
  by an administrator of the platform.

* ``UndefinedObjectException``: if the specified identification doesn't
  correspond to any enabled device registered to the platform.
