===============
``POST /route``
===============

--------
Synopsis
--------

Add a route to follow to reach a destination. A route is defined by a
path and a possible series of two or more ordered waypoints.

To follow such a route, a vehicle navigates to the nearest waypoint,
then to the next one in turn until the destination is reached.

The vehicle might not strictly follow the indicated path, thought the
organisation would received a notification, however the vehicle MUST
cross each waypoint in their given order.


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

None.

* ``mid:string`` (optional): identification of a custom map created in
  Google My Maps and which link has been shared to create this route.

* ``keep_synced`` (optional): indicate whether to keep the route
  synced with the custom map created in Google My Maps which link has
  been shared to create this route. By default, the route is not keep
  synced. This parameter requires the parameter ``mid`` to be passed.

* ``privacy_level``: indicate the visibility of this route:

    * ``public``

    * ``private``


--------------------
Request Message Body
--------------------

The HTTP request must contain the following JSON structure, unless
the query parameter ``mid`` is passed::

   {
     "name": string,
     "path": [
       {
         "latitude": decimal,
         "longitude": decimal
       },
       ...
     ],
     "waypoints": [
       {
         "latitude": decimal,
         "longitude": decimal,
         "name": string
       },
     ]
   }

where:

* ``name`` (optional): name given to this route, if any defined.

* ``path`` (required): the road-trip path that a vehicle will be
  required to follow, represented by a polyline, which is a series of
  straight lines connecting several points provided in order. All
  coordinate values are in the World Geodetic System (WGS84).

  A path is typically an open shape as the last point is not connected
  connected to the first point.

  * ``latitude`` (required): latitude-angular distance, expressed in
    decimal degrees (WGS84 datum), measured from the center of the
    Earth, of a point north or south of the Equator corresponding to
    the next point of the path.

  * ``longitude`` (required): longitude-angular distance, expressed in
    decimal degrees (WGS84 datum), measured from the center of the
    Earth, of a point east or west of the Prime Meridian corresponding
    to the next point of the path.

* ``waypoints`` (optional): a series of points along the route that a
  specified vehicle is expected to cross. A waypoint is also known as
  a control point or a checkpoint.

  * ``latitude`` (required): latitude-angular distance, expressed in
    decimal degrees (WGS84 datum), measured from the center of the
    Earth, of a point north or south of the Equator corresponding to
    the next point of the path.

  * ``longitude`` (required): longitude-angular distance, expressed in
    decimal degrees (WGS84 datum), measured from the center of the
    Earth, of a point east or west of the Prime Meridian corresponding
    to the next point of the path.

  * ``name`` (optional): name given to this waypoint, if any defined.


---------------------
Response Message Body
---------------------

None.


----------
Exceptions
----------

The platform MAY raise the following exceptions to indicate that one
or several required conditions have not been respected:
