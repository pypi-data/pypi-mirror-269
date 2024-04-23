``POST /device/(device_id)/activation``
=======================================

Synopsis
--------

Activate a mobile device with an activation code.


Request Header Fields
---------------------

.. include:: /_include/optional_authenticated_session_header_fields.inc


Request URL Bits
----------------

* ``device_id: string``: The identification of the mobile device.


Request Query Parameters
------------------------

None.


Request Message Body
--------------------

The HTTP request MUST contain the following JSON structure::

    {
      "activation_code": string,
      "location": {
        "accuracy": decimal,
        "altitude": decimal,
        "fix_time": timestamp,
        "latitude": decimal,
        "longitude": decimal
      }
    }

where:

- ``activation_code`` (required): The activation code that the client application running on the mobile device has scanned.
* ``location`` (optional): Current location of the mobile device.

  * ``accuracy`` (optional): Accuracy in meters of the mobile mobile device's location.

  * ``altitude`` (required): Altitude in meters of the mobile device's location.

  * ``fix_time`` (required): Time when the mobile device determined the information of this fix.

  * ``latitude`` (required): Latitude-angular distance, expressed in decimal degrees (WGS84 datum), measured from the center of the Earth, of a point north or south of the Equator corresponding to the mobile device's location.

  * ``longitude`` (required): Longitude-angular distance, expressed in decimal degrees (WGS84 datum), measured from the center of the Earth, of a point east or west of the Prime Meridian corresponding to the mobile device's location.


Response Message Body
---------------------

The server platform returns the following JSON form::

    {
      "account": {
        "account_id": string,
        "first_name": string,
        "full_name": string,
        "picture_id": string,
        "picture_url": string,
        "update_time": timestamp
      },
      "activation_time": timestamp,
      "app_id": string,
      "app_version": {
        "major": number,
        "minor": number,
        "patch": number
      },
      "device_id": string,
      "object_status": string,
      "security_key": string,
      "team": {
        "name": string,
        "picture_id": string,
        "picture_url": string,
        "team_id": string,
        "update_time": timestamp
      },
      "update_time": timestamp
    }

where:


* ``account`` (optional): The information about the individual user who owns this mobile device.

  * ``account_id`` (required): The identification of the user's account.

  * ``first_name``" (optional): The Forename (also known as *given name*) of the user.

  * ``full_name`` (required): The complete personal name by which the user is known.

  * ``last_name`` (optional): The surname (also known as *family name*) of the user.

  * ``picture_id`` (optional): The identification of the user's photo ID.

  * ``picture_url`` (optional): The Uniform Resource Locator (URL) that specifies the location of the user's photo ID.

  * ``update_time`` (required): The time of the most recent modification of the information of this user.

* ``activation_time`` (required): The time when the client application has been activated on the mobile device.

* ``app_id`` (required): The identification of the client application that has been activated.

* ``app_version`` (required): The current version of the client application installed on the mobile device.

* ``device_id`` (required): The identification of the mobile device.

* ``object_status`` (required): The current status of the client application installed on the mobile device.

* ``security_key`` (required): The security key generated that the client application must use to secure the communication with the cloud service.

* ``team`` (optional): The information about the organization that manages this mobile device. This attribute is only provided if the current activation status of this device is ``disabled`` or ``enabled``.

  * ``name`` (required): The name of the organization.

  * ``picture_id`` (optional): The identification of the picture that visually represents the organization, such as its logo, if any defined.

  * ``picture_url`` (optional): The Uniform Resource Locator (URL) that specifies the location of the picture representing the organization, if any defined.  The client application can use this URL and append the query parameter ``size`` to specify a given pixel resolution of the picture, such as ``thumbnail``, ``small``, ``medium``, or ``large``.

  * ``team_id`` (required): The identification of the organization.

* ``update_time`` (required): The time of the most recent modification of one or more attributes of this client application installed on the mobile device.


Exceptions
----------

The platform MAY raise the following exceptions to indicate that one or several required conditions have not been respected:

* ``DeletedObjectException``: If the specified activation code has expired.

* ``IllegalAccessException``: If the mobile device has been already activated by another organization.

* ``InvalidOperationException``: If this mobile device has been disabled or banned from the organization.

* ``UndefinedObjectException``: If the specified code doesn't refer to any activation request registered to the platform.
