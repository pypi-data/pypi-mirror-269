======================
``POST /payment/cash``
======================

--------
Synopsis
--------

Credit the account of a customer who provides cash money to an
authorized dealer:

#. The customer must first authenticated against the platform and
   he must indicate the amount of money he is giving to the
   authorized dealer.

#. The dealer must confirm this amount and he must complete the
   transaction by entering his password.


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


--------------------
Request Message Body
--------------------

The HTTP request must contains the following JSON structure::

    {
      "account_id": string,
      "amount": decimal,
      "currency": decimal
    }

where:

* ``account_id`` (required): identification of the account of the
  customer who credits his account by providing cash money to an
  authorized dealer.

* ``amount`` (required): amount of the cash money the customer
  provides to the authorized dealer.

* ``currency`` (required): ISO 4217 alphabetical code representing
  the currency of the transaction.  This alphabetic code is based on
  another ISO standard, ISO 3166, which lists the codes for country
  names.  The first two letters of the ISO 4217 three-letter code are
  the same as the code for the country name, and where possible the
  third letter corresponds to the first letter of the currency name.


---------------------
Response Message Body
---------------------

The platform returns the following JSON form::

    {
      "transaction_id": string
    }

where:

* ``transaction_id``: identification of the transaction between the
  customer and the authorized dealer.


----------
Exceptions
----------

The platform MAY raise the following exceptions to indicate that one
or several required conditions have not been respected:

* ``DeletedObjectException``: if the account of the customer has
  been deleted.

* ``DisabledObjectException``: if the account of the customer has
  been disabled.

* ``IllegalAccessException``: if the authenticated account, on
  behalf of whom the request is sent to the platform, is not an
  authorized dealer.

* ``UndefinedObjectException``: if the specified account
  identification of the customer doesn't correspond to any user
  account registered against the platform.
