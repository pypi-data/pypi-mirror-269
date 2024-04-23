=======================================
``POST /prospect/vehicle/registration``
=======================================

--------
Synopsis
--------

Register the email address of a prospect who signed-up online to the
Explorer Program and save the vehicle model of this prospect.

The Explorer Program is designed for people who want to get involved
early and help shape the future of the service.  This program is
expanding little by little, and experimenting with different ways of
bringing new Explorers into the program.

If a prospect is a Vietnam resident and is interested in joining, he
can sign up here and the responsibles of the online service let him
know if a spot opens up.


.. note::

   This request will be deprecated as soon as the service will be
   fully opened to all the users.


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

None.


--------------------
Request Message Body
--------------------

The HTTP request must contain the following JSON structure::

    {
      "email_address": string,
      "make": string,
      "model": string,
      "model_id": string
    }

where:

* ``email_address`` (required): email address of the prospect.

* ``make`` (optional): name of a manufacturer that built the
  prospect's vehicles.

* ``model`` (optional): commercial name of the model of the
  prospect's vehicle.

* ``model_id`` (optional): identification of the prospect's vehicle
  as registered on the platform.

.. note::

   Either ``model_id`` needs to be provided, either ``make`` and
   optionally ``model`` needs to be provided.


---------------------
Response Message Body
---------------------

None.


----------
Exceptions
----------

The platform MAY raise the following exceptions to indicate that one
or several required conditions have not been respected:

* ``InvalidOperationException``: if the parameter ``model_id`` or
  ``make`` has not been provided, or both of them have been provided.
