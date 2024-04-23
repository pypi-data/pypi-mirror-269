========================
``PUT /sim/(imsi)/plan``
========================

--------
Synopsis
--------

Specify the terms of the data monthly service, also known as airtime
service, of a given SIM card that enables to send and receive data and
to access information via the Internet.


---------------------
Request Header Fields
---------------------

.. include:: /_include/authenticated_session_header_fields.inc


----------------
Request URL Bits
----------------

* ``imsi:string`` (required): International Mobile Subscriber Identity
  (IMSI) as stored in the SIM card.


------------------------
Request Query Parameters
------------------------

None.


--------------------
Request Message Body
--------------------

The HTTP request must contain the following JSON structure::

    [
      {
        "activation_time": timestamp,
        "data_amount": integer
      },
      ...
    ]

where:

* ``activation_time`` (required): date and time when the SIM card has
  been activated.  Monthly subscription charges generally commence when
  the SIM card is activated, which is at the point of purchase.

* ``data_amount`` (required): monthly data usage in MB the plan allows.
  Once data usage exceeds this limit, the customer will more likely be
  charged a data overage rate.

---------------------
Response Message Body
---------------------

None.


----------
Exceptions
----------

The platform MAY raise the following exceptions to indicate that one
or several required conditions have not been respected:

* ``DeletedObjectException``: if the SIM card has been deleted.

* ``DisabledObjectException``: if the SIM card has been disabled.

* ``IllegalAccessException``: if the user on behalf of whom this
  request is sent is not the owner of this SIM card, nor a member of
  the organization that officially owns this SIM card.

* ``UndefinedObjectException``: if the specified identification
  doesn't refer to a SIM card registered to the platform.
