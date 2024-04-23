===============================
``GET /device/location/recent``
===============================

--------
Synopsis
--------

Return a list of the most recent geographical locations of the
specified devices.


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

* ``devices:list`` (required): a coma-separated list of devices
  specification.  Up to 100 are allowed in a single request.  Each
  device specified using the following format::

      imei@sync_time

  where:

  * ``imei:string`` (required): International Mobile Equipment
    Identity (IMEI) of the device to return its recent locations.

  * ``sync_time:timestamp`` (optional): indicate the earliest time
    to return locations based on their time of fix.  If not
    specified, the platform returns any available prior recent
    locations of this device, sorted by ascending order.

* ``fix_age:integer`` (optional): maximal age in seconds of the
  location fixes to be returned.

* ``limit:integer`` (optional): constrain the number of locations
  that are returned per device to the specified number.  Maximum
  value is ``100``.  The default value is ``20``.


--------------------
Request Message Body
--------------------

None.


---------------------
Response Message Body
---------------------

The HTTP request must contains the following JSON structure::

    [
      {
        "imei": string,
        "locations": [
          {
            "accuracy": decimal,
            "altitude": decimal,
            "bearing": decimal,
            "fix_time": timestamp,
            "latitude": decimal,
            "longitude": decimal,
            "provider": string,
            "speed": decimal
          },
          ...
        ],
      },
      ...
    ]

where:

* ``imei`` (required): International Mobile Equipment Identity
  (IMEI) of a device.

* ``locations`` (required): a list of geographical locations of the
  device sorted with the requested order.  Each location contains the
  following attributes:

  * ``accuracy`` (required): accuracy in meters of the device's
    location.

  * ``altitude`` (required): altitude in meters of the device's
    location.

  * ``bearing`` (optional): bearing in degrees.  Bearing is the
    horizontal direction of travel of the device, and is not related
    to the device orientation.  It is guaranteed to be in the range
    ``[0.0, 360.0]``, or it is not provided if this location does not
    have a bearing.

  * ``fix_time`` (required): time when the device determined the
    information of this fix, which time might be slightly different
    from the time when the mobile device sent the location report to
    the platform, for instance, in case of limited network
    connectivity, the mobile phone decided to cache locally this
    report before sending it eventually to the platform.

  * ``latitude`` (required): latitude-angular distance, expressed
    in decimal degrees (WGS84 datum), measured from the center of the
    Earth, of a point north or south of the Equator corresponding to
    the location.

  * ``longitude`` (required): longitude-angular distance,
    expressed in decimal degrees (WGS84 datum), measured from the
    center of the Earth, of a point east or west of the Prime
    Meridian corresponding to the location.

  * ``provider`` (required): code name of the location provider
    that reported the geographical location.

    * ``gps``: indicate that the location has been provided by a
      Global Positioning System (GPS).

    * ``network``: indicate that the location has been provided
      by an hybrid positioning system, which uses different
      positioning technologies, such as Global Positioning System
      (GPS), Wi-Fi hotspots, cell tower signals.

  * ``speed`` (optional): speed in meters/second over the ground,
    or it is not provided if this location does not have a speed.


----------
Exceptions
----------

The platform MAY raise the following exceptions to indicate that one
or several required conditions have not been respected:

* ``DeletedObjectException``: if a specified device has been deleted.

* ``DisabledObjectException``: if a specified device has been disabled.

* ``InvalidOperationException``: if a specified device is not linked to
  any account or team.

* ``UndefinedObjectException``: if a specified IMEI doesn't correspond
  to any enabled device registered against the platform.
