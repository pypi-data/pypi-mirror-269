=============
Notifications
=============

The platform sends notifications to inform users about events related
to their devices.

+-------------------------------+------------------------------------------------------------------------+
| Notification                  | Description                                                            |
+===============================+========================================================================+
| on_alert_state_changed_       | Indicate that the alert state of a vehicle has changed as reported by  |
|                               | the device mounted on this vehicle.                                    |
+-------------------------------+------------------------------------------------------------------------+
| on_battery_state_changed_     | Indicate that device has been connected to or disconnected from the    |
|                               | power source of the vehicle this device is mounted on, or the level of |
|                               | the device's battery increases or decreases.                           |
+-------------------------------+------------------------------------------------------------------------+


``on_alert_state_changed``
==========================

.. _on_alert_state_changed:

The notification ``on_alert_state_changed`` is sent whenever an alert
starts or stops.

An alert starts whenever the device detects a movement based on the
values read from a built-in motion sensor, such as a gyroscope or an
accelerometer.  An alert stops when no movement is detected after a
few seconds.

Depending on the current alert mode of the device, an alert event is
considered either as a serious threat (active mode), either as
expected (passive mode).

While active mode engaged, an alarm has to be immediately raised to
the owner of the device.  While passive mode enabled, a simple
notification is sent to the owner of the device.

The platform delivers this notification to the user who has acquired
this device and every member of his organization that manages this
device.  This notification includes a JSON payload of the following
form::

    {
      "alert_id": string,
      "device_id": string,
      "event_time": timestamp,
      "event_type": string,
      "location": {
        "accuracy": decimal,
        "altitude": decimal,
        "bearing": decimal,
        "fix_time": timestamp,
        "latitude": decimal,
        "longitude": decimal,
        "provider": string,
        "speed": decimal
      }

    }

where:

* ``alert_id`` (required): identification of the alert which is unique
  whether the alert starts or it stops.

* ``device_id`` (required): identification of the device that reported
  these alert changes.

* ``event_time`` (required): time when the device raises this alert
  event, i.e., when the alert started or when it stopped.  This time
  could be slightly different from the time when the device sent this
  alert to the platform, for instance, in case of limited network
  connectivity, the device decided to cache locally this alert before
  sending it eventually to the platform.

* ``event_type`` (required): indicate if the alert started or
  stopped:

  * ``alert_start``: the device has detected a significant movement of the
    vehicle which the device is mounted on.

  * ``alert_stop``: the device has not dectected any movement after a few
    seconds.

* ``location`` (optional): last known location of the device when this
  event occurred:

  * ``accuracy`` (required): accuracy in meters of the location.

  * ``altitude`` (required): altitude in meters of the location.

  * ``bearing`` (optional): bearing in degrees.  Bearing is the horizontal
    direction of travel of the device, and is not related to the device
    orientation.  It is guaranteed to be in the range ``[0.0, 360.0]``.

  * ``fix_time`` (required): time when the device determined the
    information of this fix.

  * ``latitude`` (required): latitude-angular distance, expressed in
    decimal degrees (WGS84 datum), measured from the center of the Earth,
    of a point north or south of the Equator corresponding to the
    location.

  * ``longitude`` (required): longitude-angular distance, expressed in
    decimal degrees (WGS84 datum), measured from the center of the Earth,
    of a point east or west of the Prime Meridian corresponding to the
    location.

  * ``provider`` (required): code name of the location provider that
    reported the location.

    * ``gps``: indicate that the location has been provided by a Global
      Positioning System (GPS).

    * ``network``: indicate that the location has been provided by an hybrid
      positioning system, which uses different positioning technologies,
      such as Global Positioning System (GPS), Wi-Fi hotspots, cell tower
      signals.

  * ``speed`` (optional): speed in meters/second over the ground.

.. note::

    A device may raise several alert changes while there is no network
    connectivity.  The device will eventually send all these alert changes
    to the platform when the connectivity is restored.  However the
    platform will only broadcast the last alert change raised by the
    device; the platform saves all the alert changes raised by the device
    in the history of this device.


``on_battery_state_changed``
============================

.. _on_battery_state_changed:

.. note::

    Only devices equipped with an internal battery can broadcast this
    notification.  A device not equipped with an internal battery is
    indeed less secure as it is not able to send any notification when it
    is disconnected from the power source of the vehicle this device is
    mounted on; the device is immediately switched off.


The notification ``on_battery_state_changed`` is sent whenever:

* the device is connected to or disconnected from the power source of
  the vehicle this device is mounted on;

* the level of the device's battery increases or decreases.

The platform delivers this notification to the user who has acquired
this device and every member of his organization that manages this
device.  This notification includes a JSON payload of the following
form::

    {
      "battery_level": decimal,
      "device_id": string,
      "event_id": string,
      "event_time": timestamp,
      "event_type": string,
      "location": {
        "accuracy": decimal,
        "altitude": decimal,
        "bearing": decimal,
        "fix_time": timestamp,
        "latitude": decimal,
        "longitude": decimal,
        "provider": string,
        "speed": decimal
      }
    }

where:

* ``battery_level`` (required): level in percentage of the battery of
  the device when this state change has been detected.

* ``device_id`` (required): identification of the device which battery
  state has changed.

* ``event_time`` (required): time when this event has been detected.

* ``event_type`` (required): indicate the exact event that occured:

  * ``battery_level_changed``: the level of the device's battery changed
    significantly from its previous level.

  * ``battery_plugged``: the battery of the device has been connected to
    the power source of the vehicle this device is mounted on.  This
    device is now charging normally.

  * ``battery_unplugged``: the battery of the device has been disconnected
    from the power source of the vehicle this device is mounted on.  The
    device's battery is discharging.  The device is going to shutdown if
    the battery level is low, leaving the vehicle unattended.

* ``location`` (optional): last known location of the device when this
  battery state change has been detected.

  * ``accuracy`` (required): accuracy in meters of the location.

  * ``altitude`` (required): altitude in meters of the location.

  * ``bearing`` (optional): bearing in degrees of the device at this
    moment.  Bearing is the horizontal direction of travel of the device,
    and is not related to the device orientation.  It is guaranteed to be
    in the range ``[0.0, 360.0]``, when provided.

  * ``fix_time`` (required): time when the  device determined
    the information of this fix.

  * ``latitude`` (required): latitude-angular distance, expressed in
    decimal degrees (WGS84 datum), measured from the center of the Earth,
    of a point north or south of the Equator corresponding to this
    location.

  * ``longitude`` (required): longitude-angular distance, expressed in
    decimal degrees (WGS84 datum), measured from the center of the Earth,
    of a point east or west of the Prime Meridian corresponding to this
    location.

  * ``provider`` (required): name of the location provider that reported
      this location.

  * ``speed`` (optional): speed in meters/second over the ground of the
    device at this moment.

















| on_device_properties_updated_ | Indicate that the properties of a  device have been updated. |
|                               | This notification includes the list of properties that have been    |
|                               | updated, and their new respective values.                           |
+-------------------------------+---------------------------------------------------------------------+
| on_playback_start_requested_  | Notify a particular device to start the playback of a sound effect. |
+-------------------------------+---------------------------------------------------------------------+
| on_playback_stop_requested_   | Notify a particular device to stop the playback of a sound effect.  |
+-------------------------------+---------------------------------------------------------------------+
| on_new_venue_suggested_       | Indicate that one or more new venues are suggested based on the     |
|                               | recent stopovers of vehicles.                                       |
+-------------------------------+---------------------------------------------------------------------+




+-------------------------------+---------------------------------------------------------------------+
| on_stopover_added             | Indicate that a stop-over, which is a brief stay in the             |
|                               | course of a journey of a particular vehicle, has been detected.     |
+-------------------------------+---------------------------------------------------------------------+
| on_stopover_updated           | Indicate that a stop-over of a particular vehicle has been updated. |
|                               | This stop-over was already detected, but not yet reviewed by the    |
|                               | owner of the vehicle, or a member of his organization, while a the  |
|                               | background job detects this stop-over from a recent journey of this |
|                               | vehicle, updating the size and the radius of the corresponding      |
|                               | centroid-cluster.                                                   |
+-------------------------------+---------------------------------------------------------------------+


``on_device_properties_updated``
================================

.. _on_device_properties_updated:

The notification ``on_device_properties_updated`` indicates that one
or more properties of a  device have been recently updated.

The platform delivers this notification to the owner of this 
device, and any member of his organization, including a JSON payload
of the following form::

    {
      "account_id": string,
      "device_id": string,
      "properties": {
        name: value,
        ...
      }
    }

where:

* ``account_id`` (required): identification of the account of the
  user who updated the specified properties of the device.

* ``device_id`` (required): identification of the device that has been
  updated the specified properties.

* ``properties`` (required): a dictionary of key/value pairs
  representing the properties of the device that have been updated.
  Refer to the properties list of a device.


``on_new_venue_suggested``
==========================

.. _on_new_venue_suggested:

The notification ``on_new_venue_suggested`` suggests new venues, based
on the activity analysis of the vehicles of an organization.  This
notification is sent to the members of the organization responsible
for managing these vehicles.

This notification invites members of the organization to review these
suggested new venues and to classify them into different categories
such as:

* a business related venue, such as a customer site. Then, later on,
  the platform will be able to notify the members of the organization
  when one of their vehicles enters or exits this venue.

* a venue that is not of interest for the organization, such as a
  restaurant, a tollbooth, a gas station, etc. The platform won't
  bother the members of the organization next time when their vehicles
  will stop by this venue, depending on the settings defined by the
  organization.

* an invalid venue detection, caused by an intense traffic on the
  journey of a vehicle of this organization, an accident on the road,
  a traffic light that stayed red for too long.  The platform will
  mark this location as an invalid suggested venue.

The platform delivers this notification to the owner of this 
device, and any member of his organization, including a JSON payload
of the following form::

    [
      {
        "altitude": decimal,
        "creation_time": timestamp,
        "latitude": decimal,
        "longitude": decimal,
        "team_id": string
        "venue_id": string
      },
      ...
    ]

where:

* ``altitude`` (required): altitude in meters of the estimated
  location of the venue.

* ``category`` (optional):

* ``creation_time`` (required): time when the platform detects this
  venue.

* ``latitude`` (required): latitude-angular distance, expressed in
  decimal degrees (WGS84 datum), measured from the center of the
  Earth, of a point north or south of the Equator corresponding to
  the estimated location of the venue.

* ``longitude`` (required): longitude-angular distance, expressed in
  decimal degrees (WGS84 datum), measured from the center of the
  Earth, of a point east or west of the Prime Meridian corresponding
  to the estimated location of the venue.

* ``team_id`` (required): identification of the organization that
  manages the vehicles from which activity the platform has detected
  this venue.

* ``venue_id`` (required): identification of this venue.










``on_stopover_added``
=====================

.. _on_stopover_added:

The notification ``on_stopover_added`` informs the owner of a vehicle,
and any member of his organization, that a brief stay in the course of
a current journey of his vehicle has been detected.

Stop-overs are determined from the locations reported by 
devices mounted on vehicles.  A background job filters all those
locations to, and groups them into centroid-based clusters such that
the squared distances from the cluster are minimized.

This notification invites the owner of the vehicle, or any member of
his organization, to review this stop-over and to indicate to the
platform whether this stop-over is of interest.  This stop-over could
be:

* a not yet identified valuable venue, such as the site of a
  customer of this organization, in which case it should be
  registered so that the platform can learn from it and provide more
  valuable information next time the vehicle will stop by this venue;

* a not yet identified venue, but not of interest for the
  organizaton's activity, such as a restaurant, a hotel.  The
  organization should report it as such so that the platform can
  learn from it and avoid bothering the organization next time the
  vehicle will stop by this venue, depending on the settings defined
  by the organization.

* caused by a traffic light or an intense traffic on the journey of
  the vehicle, in which case the organization should request the
  platform to ignore it for next times;

The platform delivers this notification to this particular device,
including a JSON payload of the following form::

    {
      "account_id": string,
      "altitude": decimal,
      "cluster_radius": decimal
      "cluster_size": integer,
      "imei": string,
      "latitude": decimal,
      "longitude": decimal,
      "team_id": string
    }

where:

* ``account_id`` (required): identification of the owner of the
  vehicle.

* ``altitude`` (required): altitude in meters of the estimated
  location of the stop-over, which is the center of the cluster.

* ``cluster_radius`` (required): the maximal distance between the
  center of the cluster and a location belonging to this cluster.

* ``cluster_size`` (required): number of locations reported by the
   device and grouped in this cluster.

* ``imei`` (required):  International Mobile Equipment Identity
  (IMEI) that uniquely identifies the  device mounted on a
  vehicle.

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

* ``team_id`` (optional): identification of the organization that
  manages the vehicle, if any defined by the owner.


* @column cluster_radius: the maximal distance between the center of *
the cluster and a location belonging to this cluster, reported
*     by the  device. *
* @column cluster_size: number of locations reported by the  *
device and grouped in this cluster. * * @column reviewer_id:
identification of the account of the user who
*     reviewed this stop-over.  This user is either the owner of the *
vehicle, either a member of the organization that manages this
*     vehicle. *
* @column venue_id: identification of a venue that corresponds to the *
location of this stop-over.  This venue could be suggested by
*     the background task responsible for determining stop-overs of *
the vehicle based on the locations reported by the 
*     device. *
* @column object_status: current status of this stop-over : * *     *
`+object-status-enabled+`: this stop-over has already been
*       identified as a venue by the owner or a member of the *
organization that manages this vehicle. * *
* `+object-status-disabled+`: this stop-over has already been *
disabled by the owner or a member of the organization that
*       manages this vehicle, as it does not correspond to a point of *
of interest (i.e, a venue). * *
* `+object-status-pending+`: this stop-over has been created * but
not yet reviewed by the owner or a member of the
*       organization that manages this vehicle.
