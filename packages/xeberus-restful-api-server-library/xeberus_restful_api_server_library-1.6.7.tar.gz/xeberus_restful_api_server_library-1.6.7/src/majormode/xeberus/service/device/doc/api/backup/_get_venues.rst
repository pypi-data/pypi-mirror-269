===============
``GET /venues``
===============

--------
Synopsis
--------

Return a list of venues related to a user, and his organization, if
any specified.

These venues are those the user or any member of his organization has
registered.  They can also be new venues suggested by the platform
based on the activity of the vehicles of the user or his organization.


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

* ``include_address:boolean`` (optional): indicate whether to
  include address information of the venues returned.  By default,
  address information is not included.

* ``include_contacts:boolean`` (optional): indicate whether to
  include contact information of the venues returned.  By default,
  contact information is not included.

* ``include_stopovers:boolean`` (optional): indicate whether to
  include brief stays in the course of a journey of vehicles.
  Stop-overs are determined from the locations reported by tracker
  devices mounted on vehicles.  A background job filters all those
  locations to, and groups them into centroid-based clusters such
  that the squared distances from the cluster are minimized.  By
  default, stopovers are not included.

* ``limit:integer`` (optional): constrain the number of venues that
  are returned to the specified number.  Maximum value is ``100``.
  The default value is ``20``.

* ``locale:locale`` (optional): locale of any textual information
  that is returned.  A locale corresponds to a tag respecting RFC
  4646, i.e., a ISO 639-3 alpha-3 code element optionally followed by
  a dash character ``-`` and a ISO 3166-1 alpha-2 code (referencing
  the country that this language might be specific to). For example:
  ``eng`` (which denotes a standard English), ``eng-US`` (which
  denotes an American English).

  .. note::

     If no locale is specified, the platform returns textual
     information in all the available translated versions.

  .. note::

     If there is textual information not available in the specified
     locale, the platform returns all the translated versions of this
     particular textual information.

* ``sync_time:timestamp`` (optional): indicate the earliest time to
  return venues based on the time of their most recent modification.
  If not specified, the platform returns any available venues, sorted
  by ascending order of their modification time.

* ``team_id:string`` (optional): the identification of an
  organization the authenticated user belongs to.  If defined, the
  platform returns the venues registered by any member who belongs to
  this organization.


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
        "address": {
          component_type: string,
          ...
        },
        "contacts": [
          [ name:string, value:string, is_primary:boolean, is_verified:boolean ],
          ...
        ],
        "creation_time": timestamp,
        "is_business_related": boolean,
        "location": {
          "accuracy": decimal,
          "altitude": decimal,
          "latitude": decimal,
          "longitude": decimal
        },
        "object_status": integer,
        "update_time": timestamp,
        "venue_id": string,
      }
    ]

where:

* ``address`` (optional): postal address of the venue, composed of
  one or more address components, which textual information is
  written in the specified locale. An address component is defined
  with a component type and its value. The component type is one of
  these:

  * ``house_number``: unique number of the  venue in the street or
    area, which eases to locate this particular venue. House
    numbering schemes vary by venue, and in many cases even within
    cities. In some areas of the world, including many remote areas,
    houses are not numbered at all, instead simply being named. In
    some other areas, this numbering can be composed of a first
    number along the street followed by a second the number along
    intersecting street, or they would adopt a system where the city
    is divided into small sections each with its own numeric code.
    The houses within that zone are then labeled based on the order
    in which they were constructed, or clockwise around the block.

  * ``street_name``: street name or odonym, i.e., an identifying
    name, given to the street where the venue is located in. The
    street name usually forms part of the address (though addresses
    in some parts of the world, notably most of Japan, make no
    reference to street names).

  * ``ward``: represent rural communes, commune-level town, and
    urban wards.

  * ``district``: represent districts in rural areas and precincts
    in urban areas.

  * ``city``

  * ``postal_code``: postal code as used to address postal mail
    within the country.

  * ``province``

  * ``recipient_name``: intended recipients name or other
    designation, which can be an individual, a business, a venue, an
    organization.

  * ``country``

* ``contacts`` (optional): list of properties such as e-mail
  addresses, phone numbers, etc., in respect of the electronic
  business card specification (vCard). The contact information is
  represented by a list of tuples of the following form::

      [ name:string, value:string, is_primary:boolean, is_verified:boolean ]

  where:

  * ``name``: type of this contact information, which can be one
    of these standard names in respect of the electronic business
    card specification (vCard):

    * ``EMAIL``: e-mail address.

    * ``PHONE``: phone number in E.164 numbering plan, an ITU-T
      recommendation which defines the international public
      telecommunication numbering plan used in the Public Switched
      Telephone Network (PSTN).

    * ``WEBSITE``: Uniform Resource Locator (URL) of a Web site.

  * ``value``: value of this contact information representing by a
    string, such as ``+84.01272170781``, the formatted value for a
    telephone number property.

  * ``is_primary``: indicate whether this contact information is
    the primary for this venue.

   * ``is_verified``: indicate whether this contact information
     has been verified, whether it has been grabbed from a trusted
     Social Networking Service (SNS), or whether through a
     challenge/response process.

* ``creation_time`` (required): time when this venue has been
  registered to the platform.

* ``is_business_related`` (optional): indicate whether this venue is
  connected to the business of the user or his organization.

* ``location`` (required): geographical coordinates of the location
  of the venue represented with the following JSON structure::

      {
        "accuracy": decimal,
        "altitude": decimal,
        "latitude": decimal,
        "longitude": decimal
      }

  where:

  * ``accuracy`` (optional): accuracy of the venue's position in
    meters.

  * ``altitude`` (optional): altitude in meters of the venue.

  * ``latitude`` (required): latitude-angular distance, expressed
    in decimal degrees (WGS84 datum), measured from the center of the
    Earth, of a point north or south of the Equator corresponding to
    the venue's location.

  * ``longitude`` (required): longitude-angular distance,
    expressed in decimal degrees (WGS84 datum), measured from the
    center of the Earth, of a point east or west of the Prime
    Meridian corresponding to the venue's location.

* ``object_status`` (required): current status of this venue.

  * ``OBJECT_STATUS_ENABLED``: this venue has already been identified
    as a venue by the user or a member of his organization.

  * ``OBJECT_STATUS_DISABLED``: this venue has already been disabled
    by the user or a member of his organization, as this location is
    not of interest.  The platform doesn't delete this record to
    remind that this location should not be suggested to the user and
    his organization anymore.

  * ``OBJECT_STATUS_PENDING``: this venue has been suggested to the
    user, but not yet reviewed by him, nor by any member of his
    organization.

* ``update_time`` (required): time of the last modification of one
  or more attributes of this venue.

  .. note::

     This time should be used by the client application to manage its
     cache of venues and to reduce the average time to access data of
     venues. When the client application needs to read venues'
     attributes, it first checks whether a copy of these data is in its
     cache. If so, the client application immediately reads from the
     cache, which is much faster than requesting these data from the
     server platform.

* ``venue_id`` (required): identification of the venue.


----------
Exceptions
----------

None.
