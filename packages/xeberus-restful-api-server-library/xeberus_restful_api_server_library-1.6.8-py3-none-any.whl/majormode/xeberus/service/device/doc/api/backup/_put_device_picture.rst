===============================
``POST /device/(imei)/picture``
===============================

--------
Synopsis
--------

Upload a new picture to graphically represent a registered device.


---------------------
Request Header Fields
---------------------

.. include:: /_include/authenticated_session_header_fields.inc

* ``Content-Type``: the content type ``multipart/form-data`` MUST be
  used for submitting the file that contain the new picture that will
  be used to graphically represent the specified tracker device.  The
  MIME multipart data stream MUST conform to
  `RFC 2388 <http://www.ietf.org/rfc/rfc2388.txt>`_.

  One and only one image file MUST be uploaded as part of MIME data
  stream.  The field name of the content-disposition header that
  qualifies this unique entry has no importance, nor does the
  original name of the image file have.

  For instance, using the command line cURL::

    curl -XPUT "http://%(API_DOMAIN_NAME)s/device/353893040040579/picture" \
         -F picture=@"~/triumph_street_triple.jpg" \
         -H 'X-Authentication: f31aa1c2-f1bd-11e1-abf1-109adda98fe0' \
         -H 'X-API-Key: f8be9c73329f11e18afd109adda98fe0' \
         -H 'X-API-Sig: 3706c4d77fcd8e99b5f1e5d22d7d7623786ce419'


----------------
Request URL Bits
----------------

* ``imei`` (required): International Mobile Equipment Identity
  (IMEI) that uniquely identifies the device to update its picture.


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

* ``IllegalAccessException``: if the account of the user on behalf
  of whom this request is sent is not allowed to update the
  properties of this device, i.e., nor the owner of this device, nor
  an administrator of the team this device belongs to, nor an
  administrator of the platform.

* ``UndefinedObjectException``: if the specified IMEI doesn't refer
  to any device registered against the platform.
