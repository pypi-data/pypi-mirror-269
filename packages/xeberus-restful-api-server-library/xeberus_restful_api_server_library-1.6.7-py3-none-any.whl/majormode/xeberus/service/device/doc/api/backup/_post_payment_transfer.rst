==========================
``POST /payment/transfer``
==========================

--------
Synopsis
--------

Register a payment transfer (*giro*) from the bank account of the
authenticated user to the bank account of the company that operates
this service.  This payment transfer and instigated by the payer.

The registration of a payment transfer requires to provide the
reference of the transaction instigated by the user on the secured
Web site operated by his bank.  This reference was given by this Web
site when the user completed the funds transfer.  There is no need to
provide the amount of the transaction, nor the currency, as this
information will be automatically retrieved later from the details of
this transaction in the account statement of the bank account of the
company that operates this service.

The platform checks whether this payment transfer is already effective
by checking the account statements of the company's bank account.  If
this transfer is verified, the platform credits the user's account
with the amount of the transaction, otherwise the platform marks this
transaction as ``pending``.


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

The HTTP request must contain the following JSON structure::

    {
      "reference": string
    }

where:

* ``reference`` (required): reference of the transaction that the
  secured Web site operated by the bank indicated to the user when
  the latter completed the funds transfer.


---------------------
Response Message Body
---------------------

The platform returns the following JSON form::

    {
      "transaction_id": string
    }

where:

* ``transaction_id``: global identification of the transaction
  within the platform.


----------
Exceptions
----------

The platform MAY raise the following exceptions to indicate that one
or several required conditions have not been respected:

* ``DeletedObjectException``: if the account of the user has been
  deleted.

* ``DisabledObjectException``: if the account of the user has been
  disabled.

* ``InvalidOperationException``: if this transfer has been already
  registered against the platform.

* ``UndefinedObjectException``: if the specified account
  identification of the user doesn't correspond to any user account
  registered against the platform.
