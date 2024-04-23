``POST /device/(device_id)/location/event``
===========================================

Synopsis
--------

Report geographic location updates of a mobile device.

This report includes one or more geographic locations depending on the number of location updates of this mobile device between two consecutive reports transmitted to the cloud service.


Request Header Fields
---------------------

.. include:: /_include/optional_authenticated_session_header_fields.inc


Request URL Bits
----------------

* ``device_id:string``: The identification of the mobile device that reports these geographic location updates.


Request Query Parameters
------------------------

None.


--------------------
Request Message Body
--------------------

The HTTP request must contains the following JSON structure::

    {
      "events": [
        {
          "accuracy": decimal,
          "altitude": decimal,
          "bearing": decimal,
          "event_ref": string,
          "event_time": string,
          "fix_time": timestamp,
          "latitude": decimal,
          "longitude": decimal,
          "payload": json,
          "provider": string,
          "mileage": decimal,
          "network_type": string,
          "report_id": string,
          "satellites": string,
          "speed": decimal
        },
        ...
      ],
      "token": string
    }

where:

* ``events`` (required): A list of location update events:

  * ``accuracy`` (required): The accuracy in meters of the geographic location.

  * ``altitude`` (required): The altitude in meters of the geographic location.

  * ``bearing`` (optional): The bearing in degrees of the mobile device.  Bearing is the horizontal direction of travel of the tracker mobile device, and is not related to the device orientation.  It is guaranteed to be in the range ``[0.0, 360.0]``, or ``null`` if this device does not have a bearing.

  * ``event_ref`` (required): The reference of this event as given by the client application running on the mobile device that reported this event.

    This information is used to detect events that the mobile device would report multiple times.  This happens when network outage occurs after the client application reported successfully a batch of events, but the network connection with the cloud service timed out before the client application had the chance to receive the acknowledgement from the cloud service.  Therefore, the client application reattempts to report one more time these events.

  * ``event_time`` (required): The time when this event occurred, which could be slightly different from the time when the device sent this event to the platform, for instance, in case of limited network connectivity, the device decided to cache locally this event before sending it eventually to the platform.

  * ``fix_time`` (required): The time when the mobile device determined the information of this fix.

  * ``latitude`` (required): The latitude-angular distance, expressed in decimal degrees (WGS84 datum), measured from the center of the Earth, of a point north or south of the Equator.

  * ``longitude`` (required): The longitude-angular distance, expressed in decimal degrees (WGS84 datum), measured from the center of the Earth, of a point east or west of the Prime Meridian.

  * ``network_type`` (optional): A string representation of the network connection at the time this location fix has been determined by the mobile device.of this location fix::

         MNCMCC:type[:subtype]

    where:

    * ``MNCMCC:string`` (required): A Mobile Network Code (MNC) used in combination with a Mobile Country Code (MCC) (also known as a "MCC/MNC tuple") to uniquely identify the telephony operator of the mobile device.

    * ``type:string`` (required): A human-readable name that describes the type of the network that the device is connected to, such as ``wifi``, ``mobile``, ``unknown``.

    * ``subtype:string`` (optional): A human-readable name that describes the subtype of this network when applicable.  Network of type ``wifi`` has not subtype.  Network of type ``mobile`` can have a subtype such as ``egde``, ``hsdpa``, etc.

  * ``mileage`` (optional): The total distance travelled by the mobile device since the application has been installed and executed on this device.  This mileage is calculated by the device itself based on the location changes its internal GPS determined over the time.  This mileage might not correspond to the mileage displayed by the odometer of the vehicle this device is mounted on.

  * ``payload`` (optional): A JSON expression of additional information that the mobile device provided within this report.

  * ``provider`` (required): The type of the location provider that reported this geographic location:

    * ``fused``: The location API in Google Play services that combines different signals to provide the location information.

    * ``gps``: This provider determines location using satellites (Global
      Positioning System (GPS).

    * ``network``: This provider determines location based on availability of cell towers and Wi-Fi access points.  Results are retrieved by means of a network lookup.

    * ``passive``: A special location provider for receiving locations without actually initiating a location fix.  This provider can be used to passively receive location updates when other applications or services request them without actually requesting the locations yourself.  This provider will return locations generated by other providers.

  * ``report_id`` (required): The identification of this location update report.

  * ``satellites`` (optional): A string representation of the information about the satellites that were used to calculate this geographic location fix::

       (azimuth:elevation:PRN:SNR),...

    where:

    * ``azimuth:float``: The azimuth of the satellite in degrees.

    * ``elevation:float``: The elevation of the satellite in degrees.

    * ``PRN:integer``: The Pseudo-Random Number (PRN) for the satellite.

    * ``SNR:float``: The signal to Noise Ratio (SNR) for the satellite.

  * ``speed`` (optional): The speed in meters/second over the ground, or ``null`` if this location does not have speed.

* ``token``: (required): A "number used once" (nonce) -- also known as pseudo-random number -- encrypted with the security key generated by the cloud service and shared with the client application.  This nonce is used to verify the authentication of the mobile device in order to prevent spoofing attack.


Response Message Body
---------------------

None.


Exceptions
----------

The platform MAY raise the following exceptions to indicate that one or several required conditions have not been respected:

* ``DeletedObjectException``: If the mobile device has been deleted.

* ``DisabledObjectException``: If the mobile device has been disabled.

* ``IllegalAccessException``: If the given seed is invalid.

* ``InvalidArgumentException``: If one or more reports identify a mobile device different from the URL bit ``device_id``.

* ``InvalidOperationException``: If the mobile device has not been activated by the user or an administrator of the organization officially responsible for this device.

* ``UndefinedObjectException``: If the specified identification doesn't correspond to any enabled mobile device registered to the platform.
