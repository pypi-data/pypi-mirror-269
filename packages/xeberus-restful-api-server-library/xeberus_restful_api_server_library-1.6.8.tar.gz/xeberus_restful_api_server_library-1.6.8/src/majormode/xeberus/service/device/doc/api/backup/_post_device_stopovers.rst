================================
``POST /device/(imei)/stopover``
================================

--------
Synopsis
--------

Report brief stays in the course of a journey of a vehicle. Stop-overs
are determined from the locations reported by tracker devices mounted
on vehicles.

A background job filters all those locations to, and groups them into
centroid-based clusters such that the squared distances from the
cluster are minimized.

Only the owner of the vehicle, or a member of the organization that
manages the vehicle, if any defined by the owner, is allowed to
review stop-overs of this vehicle.  If the ownership of the vehicle
changes from a user to another, the previous stop-overs of the
vehicle MUST NOT be accessible to the new owner, for privacy reason.

.. note::

   This request is restricted to a botnet account usage only.


---------------------
Request Header Fields
---------------------

.. include:: /_include/anonymous_session_header_fields.inc


----------------
Request URL Bits
----------------

* ``imei:string``: International Mobile Equipment Identity (IMEI)
  that uniquely identifies the tracker device mounted on a vehicle.

------------------------
Request Query Parameters
------------------------

None.


--------------------
Request Message Body
--------------------

The HTTP request must contains the following JSON structure::

    [
      {
        "altitude": decimal,
        "cluster_radius": decimal
        "cluster_size": integer,
        "latitude": decimal,
        "longitude": decimal
      },
      ...
    ]

where:

* ``altitude`` (required): altitude in meters of the estimated
  location of the stop-over, which is the center of the cluster.

* ``cluster_radius`` (required): the maximal distance in meters
  between the center of the cluster and a location belonging to the
  cluster of this stopover.

* ``cluster_size`` (required): number of locations reported by the
  tracker device and grouped in the cluster of this stopover.

* ``latitude`` (required): latitude-angular distance, expressed in
  decimal degrees (WGS84 datum), measured from the center of the
  Earth, of a point north or south of the Equator corresponding to
  the estimated location of the stop-over, which is the center of the
  cluster.

* ``longitude`` (required): longitude-angular distance, expressed in
  decimal degrees (WGS84 datum), measured from the center of the
  Earth, of a point east or west of the Prime Meridian corresponding
  to the estimated location of the stop-over, which is the center of
  the cluster.


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

* ``InvalidOperationException``: if the device is not linked to any
  account or team.

* ``IllegalAccessException``: if the account on behalf of these
  stop-overs are submitted is not a botnet account.

* ``UndefinedObjectException``: if the specified IMEI doesn't
  correspond to any enabled device registered against the platform.
