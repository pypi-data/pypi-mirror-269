==================================
``GET /device/activation/request``
==================================

--------
Synopsis
--------

Return up to 100 device activation requests that are still pending,
worth of extended information.

The application installed in a mobile tracker device MUST
automatically send a handshake to the platform every time its starts
running.

The first handshake ever of the device requests the platform to
activate the device.  Meanwhile, the device's activation is pending;
the device cannot access all the services supported by the platform
until its activation is fully completed and the device is enabled.

.. note::

   the user on behalf of whom the list of device activation requests
   is retrieved MUST be an administrator of the platform, otherwise
   the exception ``IllegalAccessException`` is raised.


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

* ``limit`` (optional): constrain the number of device activation
  requests that are returned to the specified number.  If not
  specified, the default value is ``20``.  The maximum value is
  ``100``.

* ``offset`` (optional): require to skip that many device activation
  requests before beginning to return device activation requests.
  Default value is ``0``. If both ``offset`` and ``limit`` are
  specified, then ``offset`` device activation requests are skipped
  before starting to count the ``limit`` device activation requests
  that are returned.


--------------------
Request Message Body
--------------------

None.


---------------------
Response Message Body
---------------------

The platform returns the following JSON form::

    [
      {
        "accuracy": decimal,
        "altitude": decimal,
        "fix_time": timestamp,
        "imei": string,
        "imsi": string,
        "latitude": decimal,
        "longitude": decimal,
        "provider": string,
        "creation_time": timestamp
      },
      ...
    ]

where:

* ``accuracy`` (optional): accuracy in meters of the last known
  location of the device.

* ``altitude`` (optional): altitude in meters of the last known
  location location of the device.

* ``fix_time`` (optional): time when the device has determined the
  information of the fix of the last known location.

* ``imei`` (required): International Mobile Equipment Identity
  (IMEI) that uniquely identifies the device.

* ``imsi`` (required): International Mobile Subscriber Identity
  (IMSI) of the SIM card attached to the device.

* ``latitude`` (optional): latitude-angular distance, expressed in
  decimal degrees (WGS84 datum), measured from the center of the
  Earth, of a point north or south of the Equator corresponding to
  the last known location of the device.

* ``longitude`` (optional): longitude-angular distance, expressed in
  decimal degrees (WGS84 datum), measured from the center of the
  Earth, of a point east or west of the Prime Meridian corresponding
  to the last known location of the device.

* ``provider`` (optional): code name of the location provider that
  reported the last known location of the device:

  * ``gps``: indicate that the location has been provided by a
    Global Positioning System (GPS).

  * ``network``: indicate that the location has been provided by
    an hybrid positioning system, which uses different positioning
    technologies, such as Global Positioning System (GPS), Wi-Fi
    hotspots, cell tower signals.

* ``creatin_time`` (required): time when the device has been
  registered.


----------
Exceptions
----------

The platform MAY raise the following exceptions to indicate that one
or several required conditions have not been respected:

* ``DeletedObjectException``: if the user account has been deleted.

* ``DisabledObjectException``: if the user account has been disabled.

* ``IllegalAccessException``: if the authenticated user is not an
  administrator of the platform.

* ``UndefinedObjectException``: if the specified identification
  doesn't refer to a user account registered against the platform.
