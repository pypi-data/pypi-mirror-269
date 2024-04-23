============================
``DELETE /venue/(venue_id)``
============================

--------
Synopsis
--------

Soft delete the specified venue to prevent the platform to trigger
events that would occur at the same location of this venue.  The
venue is then removed from the list of venues that the platform is
actively monitoring.

A soft delete also prevents the platform from detecting this location,
based on future stopovers of vehicles, as a possible new venue to be
suggested to the organisation that manages these vehicles.


---------------------
Request Header Fields
---------------------

.. include:: /_include/authenticated_session_header_fields.inc


----------------
Request URL Bits
----------------

* ``venue_id``: identification of the venue to ignore.


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

None.


----------
Exceptions
----------

The platform MAY raise the following exceptions to indicate that one
or several required conditions have not been respected:

* ``DeletedObjectException``: if the venue has been deleted.

* ``DisabledObjectException``: if the venue has been disabled.

* ``IllegalAccessException``: if the account on behalf of whom this
  venue is ignored is not the account who or an administrator of the
  organisation that registered this venue.

* ``UndefinedObjectException``: if the specified identification doesn't
  correspond to a venue registered on behalf of this account or one of
  the organisations this user belongs to.
