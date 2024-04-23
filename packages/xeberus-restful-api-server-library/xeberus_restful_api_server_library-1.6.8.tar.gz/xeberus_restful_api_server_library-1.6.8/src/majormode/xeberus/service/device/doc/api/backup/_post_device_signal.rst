==============================
``POST /device/(imei)/signal``
==============================

--------
Synopsis
--------

Post a collection of signals that the device has scanned nearby a
location the vehicle stops by.

A signal scan corresponds to a collection of signals that the device
has gathered from different sources nearby, such as Wi-Fi hotspots or
cell towers, at a given geographic location and at a particular time,
also known as a "fix".

A scan is used to define a fingerprint of a possible point of interest
the vehicle stops by.


---------------------
Request Header Fields
---------------------

.. include:: /_include/anonymous_session_header_fields.inc


----------------
Request URL Bits
----------------

* ``imei``: International Mobile Equipment Identity (IMEI) of the
  device submits this signal scan.


------------------------
Request Query Parameters
------------------------

* ``s`` (required): a seed, which is a "number used once" (nonce) --
  also known as pseudo-random number -- encrypted with some
  identifications of the mobile device.  For further information
  about these specific identifications, please contact the server
  platform development team.

  .. note::

  If no seed is provided, the function doesn't tag this signal scan
  with the user account which this device might be linked to; the
  device is considered being in development mode.


--------------------
Request Message Body
--------------------

The HTTP request must contains the following JSON structure::

    {
      "accuracy": decimal,
      "altitude": decimal,
      "fix_time": timestamp,
      "latitude": decimal,
      "longitude": decimal,
      "provider": string,
      "cell_towers": [
        __cell_towers__,
         ...
      ],
      "wifi_hotspots": [
        __wifi_hotspots__,
        ...
      ]
    }

where:

* ``accuracy`` (required): accuracy in meters of the device's
  location.

* ``altitude`` (required): altitude in meters of the device's location.

* ``fix_time`` (required): time when the device determined the
  information of this fix, which time might be slightly different
  from the time when the mobile device sent the location report to
  the platform, for instance, in case of limited network
  connectivity, the mobile phone decided to cache locally this report
  before sending it eventually to the platform.

* ``latitude`` (required): latitude-angular distance, expressed in
  decimal degrees (WGS84 datum), measured from the center of the
  Earth, of a point north or south of the Equator corresponding to
  the device's location.

* ``longitude`` (required): longitude-angular distance, expressed in
  decimal degrees (WGS84 datum), measured from the center of the
  Earth, of a point east or west of the Prime Meridian corresponding
  to the device's location.

* ``provider`` (required): code name of the location provider that
  reported the geographical location of the device.

  * ``gps``: indicate that the location has been provided by a
    Global Positioning System (GPS).

  * ``network``: indicate that the location has been provided by
    an hybrid positioning system, which uses different positioning
    technologies, such as Global Positioning System (GPS), Wi-Fi
    hotspots, cell tower signals.

* ``cell_towers`` (optional): a list of signals from distinct
  cellular towers that have been detected by the device.

* ``wifi_hotpots`` (optional): a list of signals gathered from
  distinct Wi-Fi hotspots that the device scanned.

The attribute ``cell_towers`` provides information about signals
gathered from neighboring cell towers.  It corresponds to an array of
dictionaries, each instance describing a signal received from a
particular cell tower::

    {
      "cid": integer,
      "is_connected": boolean,
      "lac": integer,
      "mcc": integer,
      "mnc": integer,
      "signal_level": integer
    }

where

 * ``cid`` (required): unique identifier of the cell tower.

* ``is_connected`` (optional): indicate whether the device was
  connected to this cell tower when the signal was gathered.

* ``lac`` (required): Local Area Code (LAC) of the cell tower.

* ``mcc`` (required): Mobile Country Code (MCC) of the telephony
  operator that operates this cell tower.

* ``mnc`` (required): Mobile Network Code (MCC) of the telephony
  operator that operates this cell tower.

* ``signal_level`` (optional): level of the radio signal.  This
  level is expressed in dBm.


The attribute ``wifi_hotspots`` provides information about signals
gathered from Wi-Fi hotspots nearby.  It corresponds to an array of
dictionaries, each of them describing a signal received from a
particular Wi-Fi hostspot::

    {
      "bssid": string,
      "frequency": integer,
      "is_connected": boolean,
      "signal_level": integer,
      "ssid": string
    }

where:

* ``bssid`` (required): Basic Service Set Identifier (BSSID) that
  uniquely identifies the Wi-Fi hotspot.

* ``frequency`` (optional): frequency in MHz of the channel over
  which the mobile phone was communicating with the Wi-Fi hotspot.

* ``is_connected`` (optional): indicate whether the mobile phone was
  connected to this Wi-Fi hotspot when this signal was gathered.

* ``signal_level`` (optional): level of the device signal.  This
  level is expressed in dBm.

* ``ssid`` (optional): Service Set Identifier (SSID), which is a
  friendly name that identifies a particular 802.11 wireless LAN.

.. note::

   At least, one of the following sets of information,
   ``cell_towers`` or ``wifi_hotspots``, MUST contain one or more
   entries.


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

* ``IllegalAccessException``: if the given seed is invalid.

* ``InvalidOperationException``: if the device is not linked to any
  account or team, or if none of the attributes ``cell_towers`` or
  ``wifi_hotspots`` has been provided or are both empty.

* ``UndefinedObjectException``: if the specified IMEI doesn't
  correspond to any enabled device registered against the platform.
