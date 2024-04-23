``GET /device``
===============

Synopsis
--------

Return a list of mobile devices, worth of extended information, that belongs to the authenticated user or the specified organization.


Request Header Fields
---------------------

.. include:: /_include/authenticated_session_header_fields.inc


Request URL Bits
----------------

None.


Request Query Parameters
------------------------

* ``include_apps``

* ``include_location``


* ``limit: number``: Constrain the number of records that are returned to the specified number.  Default value is ``20``. Maximum value is ``100``.

* ``offset: number``: Require to skip that many records before beginning to return records to the client.  Default value is ``0``.  If both ``offset`` and ``limit`` are specified, then ``offset`` records are skipped before starting to count the limit records that are returned.

* ``sync_time: timestamp``: Indicate the earliest non-inclusive time to filter the devices of this user based on the update time of their properties.  If not specified, no time as lower bounding filter is applied, meaning that all the devices could possibly be returned.

* ``team_id: string``: The identification of an organization that the authenticated user belongs to.  The user must be an administrator of this organization.

Request Message Body
--------------------

None.


Response Message Body
---------------------

The HTTP request must contains the following JSON structure::

    [
      {
        "apps": [
          "activation_time": timestamp,
          "app_id": string,
          "app_name": string,
          "app_version": string,
          "object_status": string,
          "update_time": timestamp
        ],
        "battery_level": decimal,
        "device_id": string,
        "is_battery_plugged": boolean,
        "keepalive_time": timestamp,
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
        "mac_address": string,
        "object_status": string,
        "os_name": string,
        "os_version": version,
        "serial_number": string,
        "update_time": timestamp
      },
      ...
    ]

where:

* ``apps`` (required): The list of client applications that have been once installed on the device, and their respective version.

  * ``activation_time`` (required): The time when the client application has been activated on the mobile device.

  * ``app_id`` (required): The identification of the client application that have been once installed on the device, and their respective version.

  * ``app_name`` (required): The name of the client application.

  * ``app_version`` (required): The current version of the client application.

  * ``object_status`` (required): The current status of this client application on the device.

    * ``enabled``: The application has been enabled by the user or an administrator of the organization that owns this device.

    * ``deleted``: The application has been deactivated on this mobile device by the server platform, for instance, when the ownership of the device has been transferred to another individual user or organization.

    * ``disabled``: The application has been deactivated by the individual user or an administrator of the organization that owns this device.

  * ``update_time`` (required): The time of the most recent update of one or more properties of this client application.

* ``battery_level`` (required): The current level in percentage of the battery of the device.

* ``device_id`` (required): The identification of the device.

* ``device_model`` (required): The end-user visible name of mobile device model.

* ``is_battery_plugged`` (required): Indicate if the battery of the device is plugged in a power source.

* ``keepalive_time`` (optional): The time of the last keep-alive (KA) message sent by the device.

* ``location`` (required): The last known location of the device:

  * ``accuracy`` (required): The accuracy in meters of the location.

  * ``altitude`` (required): The altitude in meters of the location.

  * ``bearing`` (optional): The bearing in degrees of the device.  Bearing is the horizontal direction of travel of the device, and is not related to the device orientation.  It is guaranteed to be in the range ``[0.0, 360.0]``, or it is not provided if this location does not have a bearing.

  * ``fix_time`` (required): The time when the device determined the information of this fix, which time might be slightly different from the time when the mobile device sent the location report to the cloud service, for instance, in case of limited network connectivity, the mobile phone decided to cache locally this report before sending it eventually to the cloud service.

  * ``latitude`` (required): The latitude-angular distance, expressed in decimal degrees (WGS84 datum), measured from the center of the Earth, of a point north or south of the Equator corresponding to the location.

  * ``longitude`` (required): The longitude-angular distance, expressed in decimal degrees (WGS84 datum), measured from the center of the Earth, of a point east or west of the Prime Meridian corresponding to the location.

  * ``provider`` (required): The code name of the location provider that reported the geographical location.

    * ``fused``: The location API in Google Play services that combines different signals to provide the location information.

    * ``gps``: This provider determines location using satellites (Global
      Positioning System (GPS).

    * ``network``: This provider determines location based on availability of cell towers and Wi-Fi access points.  Results are retrieved by means of a network lookup.

    * ``passive``: A special location provider for receiving locations without actually initiating a location fix.  This provider can be used to passively receive location updates when other applications or services request them without actually requesting the locations yourself.  This provider will return locations generated by other providers.

    * ``gps``: Indicate that the location has been provided by a Global Positioning System (GPS).

  * ``speed`` (optional): The speed in meters/second over the ground, or it is not provided if this location does not have a speed.

* ``mac_address`` (required): The Media Access Control (MAC) address of the mobile device.

* ``object_status`` (required): The current status of this device:

  * ``deleted``: This device has been suspended by an administrator of the cloud service. All services for this device are currently inaccessible.

  * ``disabled``: This device has been deactivated by the individual user who owns it or an administrator of the organization that manages this device.

  * ``enabled``: This device is activated and is expected to operate properly.

  * ``pending``: This device has not been activated yet by an individual user or an organization.

* ``os_name``: The name of the operating system of the mobile device.

* ``os_version`` (required): The version of the operating system of the mobile device.  This information may be updated from time to time when the operating system of the device is upgraded.

* ``serial_number``: The hardware serial number of the mobile device. It corresponds to a unique number assigned by the manufacturer to help identify an individual device.

  .. note:: Because the operating system of the mobile device may restrict access to persistent device identifiers, the serial number of the mobile device may not be provided.

* ``update_time`` (required): The time of the most recent modification of one or more properties of this device.


Exceptions
----------

None.
