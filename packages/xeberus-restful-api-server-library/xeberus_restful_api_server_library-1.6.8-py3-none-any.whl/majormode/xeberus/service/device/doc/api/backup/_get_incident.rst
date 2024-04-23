===============================
``GET /incident/(incident_id)``
===============================

--------
Synopsis
--------

Return the specified incident, worth of extended information, that
occurs when the vehicle of a user collides with another vehicle,
pedestrian, animal, road debris, or other stationary obstruction.


---------------------
Request Header Fields
---------------------

.. include:: /_include/optional_authenticated_session_header_fields.inc


----------------
Request URL Bits
----------------

None.


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

The platform returns the following JSON form::

    {
      "area": [
        {
          "area_id": string,
          "area_name": string,
          "area_level": integer
        },
        ...
      ],

      "damage_severity": integer,

      "driver": {
        "account_id": string,
        "fullname": string,
        "picture_id": string,
        "picture_url": string,
        "update_time": timestamp
      },

      "force_direction": decimal,
      "incident_id": string,
      "incident_time": timestamp,
      "locale": string,

       "location": {
        "accuracy": decimal,
        "altitude": decimal,
        "latitude": decimal,
        "longitude": decimal
      },

      "timezone_name": string,
      "timezone_offset": integer,

      "vehicle": {
        "make": string,
        "model": string,
        "model_id": string,
        "year": integer,
        "plate_number": string,
        "picture_id": string,
        "picture_url": string
      },

      "vehicle_bearing": decimal,
      "vehicle_speed": decimal
    }

where:


* ``damage_severity`` (required): describe the severity of the damage
  received. Should be reported with a single–digit numeric character
  between 0–7.

* ``force_direction`` (required): describe the direction from which
  the vehicle damage was received in comparison to the numbers on a
  clock. Should be shown with a 1 or 2–digit numeric character (1–12).
  It represents the *impact point*.

* ``vehicle_bearing`` (optional): indicate the direction of travel of
  the vehicle when the incident occurred.

* ``models`` (required): the last version of the list of vehicles
  models supported by the platform.

  * ``make`` (required): name of the manufacturer that built this
    vehicle model.

  * ``model`` (required): commercial name of the model of this
    vehicle.

  * ``model_id`` (required): identification of this particular
    vehicle model.

  * ``year`` (optional): describe approximately when this vehicle
    model was built.

* ``update_time`` (required): time of the most recent modification
  of one or more vehicle models of this list.


----------
Exceptions
----------

The platform MAY raise the following exceptions to indicate that one
or several required conditions have not been respected:

* ``IllegalAccessException``: if the specified login session doesn't belong to the specified user.

* ``UndefinedObjectException``: if the specified identification doesn't
  refer to any incident registered to the platform.
