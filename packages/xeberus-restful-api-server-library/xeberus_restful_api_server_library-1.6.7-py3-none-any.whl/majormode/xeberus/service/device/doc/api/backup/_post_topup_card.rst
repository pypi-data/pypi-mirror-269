====================
``POST /topup-card``
====================

--------
Synopsis
--------

Register a list of purchased credit card used to recharge the credit
of a Subscriber Identification Module (SIM) card with the value of
the top-up, like a voucher.  It generally corresponds to a scratch
card sold by a telephony operator or associated dealers.

A scratch card is a card made of paper-based  card, or plastic, with
hidden information printed on it -- a magic code --, covered by an an
opaque substance that can be scratched off relatively easily, while
resistant to normal abrasion.

A scratch card corresponds to a certain amount of virtual money that
is used to credit the wallet of the account of the user who bought
this card for the same amount of money.


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

The request must contain a JSON form containing the properties of the
top-up card to register::

    [
      {
        "credit_amount": float,
        "currency_code": string,
        "expiration_time": timestamp,
        "magic_code": string,
        "operator_code": string,
        "serial_number": string
      },
      ...
    ]

where:

* ``credit_amount`` (required): amount of virtual money that is used
  to credit SIM cards attached to tracker devices.

* ``currency_code`` (required): ISO 4217 alphabetical code
  representing the currency of the transaction.  This alphabetic code
  is based on another ISO standard, ISO 3166, which lists the codes
  for country names.  The first two letters of the ISO 4217
  three-letter code are the same as the code for the country name,
  and where possible the third letter corresponds to the first letter
  of the currency name.

* ``expiration_time`` (optional): time of expiration of this top-up
  card.

* ``magic_code`` (required): hidden information printed on the top-
  up card to communicate to the telephony operator to credit the
  amount of virtual money of this top-up card to the SIM card of the
  device.

* ``operator_code`` (required): combination of the Mobile Country
  Code (MCC) and Mobile Network Code (MCC) of the telephony operator
  that provides this top-up card.

* ``serial_number`` (required): serial number of a top-up card,
  visible, printed on the top-up card, mainly used for proving the
  authentication of the scratch card.


---------------------
Response Message Body
---------------------

The platform returns a list of the specified top-up cards that have
been already registered, if any::

    [
      {
        "operator_code": string,
        "serial_number": string
      },
      ...
    ]

where:

* ``operator_code`` (required): combination of the Mobile Country
  Code (MCC) and Mobile Network Code (MCC) of the telephony operator
  that provides this top-up card.

* ``serial_number`` (required): serial number of a top-up card,
  visible, printed on the top-up card, mainly used for proving the
  authentication of the scratch card.


----------
Exceptions
----------

The platform MAY raise the following exceptions to indicate that one
or several required conditions have not been respected:

* ``IllegalAccessException``: if the user on behalf of these top-up
  cards are registered has not a botnet account.
