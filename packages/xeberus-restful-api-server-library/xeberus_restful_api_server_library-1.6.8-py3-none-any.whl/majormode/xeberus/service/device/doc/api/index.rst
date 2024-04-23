Device Service
==============

.. toctree::
   :hidden:

    get_devices
    post_device_activation_code
    post_device_activation_code_generation
    post_device_battery_event
    post_device_handshake
    post_device_keepalive_event

Introduction
------------

A mobile device is a hand-held GPS unit, or a device mounted on a motorized vehicle, that makes use of the Global Positioning System (GPS) for navigational assistance and for tracking a vehicle's movements and determine its location.

The recorded location data are initially stored within the tracking unit and eventually transmitted to the Location-Based Service (LBS) platform using the cellular or Wi-Fi modem embedded in the unit.  This allows the location to be displayed against a digital map backdrop either in real time or when analyzing the track later.

For security reason, the International Mobile Equipment Identity (IMEI) of a device is not communicated to the end-user; this identification contains information that can reveal the manufacturer and the model of the device.  Instead, the device is given a hashed version of the IMEI that is displayed to the end-user.

.. note:: Starting with Android API level 29, persistent device identifiers are guarded behind additional restrictions.  Device's IMEI, and other identifiers such Integrated Circuit Card IDentifier (ICCID) and International Mobile Subscriber Identity (IMSI) stored in the SIM card inside the mobile device, are not available anymore.

A mobile device needs to be activated before it can start to operate.  More exactly a client application running on the mobile device needs to be activated to operates with server platform.  The activation of this client application corresponds to the registration of this client application and the mobile device on on behalf of an individual user or an organization.  An individual user or an administrator of an organization needs to request the server platform to generate an activation code.  This code is generally displayed as a QR code by a Web or mobile administration application that is granted access to the server platform.  The user then scans this QR code with the client application that transmits the value (the activation code) to the server platform.


Endpoints
---------

- :doc:`get_devices`: Return a list of mobile devices, worth of extended information, that belongs to the authenticated user or the specified organization.

- :doc:`post_device_activation_code`: Activate a mobile device providing an activation code.

- :doc:`post_device_activation_code_generation`: Request a code to activate one or more mobile devices.

- :doc:`post_device_handshake`: Establish the connection between a mobile device and the platform before normal communication begins.

- :doc:`post_device_keepalive_event`: Send a keep-alive (KA) message to check that the link between the device and the cloud service is operating, and to inform that the client application is running properly.

- :doc:`post_device_battery_event`: Report one or more battery state changes of a device.

- :doc:`post_device_location_event`: Report geographical location updates of a mobile device.
