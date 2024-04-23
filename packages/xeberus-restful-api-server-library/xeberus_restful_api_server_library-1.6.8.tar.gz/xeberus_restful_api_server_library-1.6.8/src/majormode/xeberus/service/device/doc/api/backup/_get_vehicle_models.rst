======================
``GET /vehicle/model``
======================

--------
Synopsis
--------

Return the list of vehicle models currently supported by the platform.


---------------------
Request Header Fields
---------------------

.. include:: /_include/anonymous_session_header_fields.inc


----------------
Request URL Bits
----------------

None.


------------------------
Request Query Parameters
------------------------

* ``make`` (optional): the name of a particular manufacturer that
  builds vehicles.

* ``sync_time`` (optional): indicate the time of the last version of
  the list of vehicle models cached by the client application. This
  time MUST be expressed in accordance with
  `RFC 3339 <http://www.ietf.org/rfc/rfc3339.txt>`_. If this time
  corresponds to the most recent version of the list of vehicle
  models registered, the platform returns an empty list, otherwise
  the platform returns the most recent version of the list of vehicle
  models. If this parameter is not provided, the platform always
  returns the most recent version of the list of vehicle models.

* ``year`` (optional): describe approximately when vehicles were
  built, and usually indicates the coinciding base specification
  (design revision number) of vehicles.  This is done for the simple
  reason of making the vehicles more easily distinguished.


--------------------
Request Message Body
--------------------

None.


---------------------
Response Message Body
---------------------

The platform returns the following JSON form::

    {
      "models": [
        {
          "make": string,
          "model": string,
          "model_id": string,
          "year": integer
        },
        ...
      ],
      "update_time": timestamp
    }

where:

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

None.
