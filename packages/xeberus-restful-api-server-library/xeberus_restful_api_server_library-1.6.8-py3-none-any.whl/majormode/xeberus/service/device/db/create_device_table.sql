/**
 * Copyright (C) 2019 Majormode.  All rights reserved.
 *
 * This software is the confidential and proprietary information of
 * Majormode or one of its subsidiaries.  You shall not disclose this
 * confidential information and shall use it only in accordance with the
 * terms of the license agreement or other applicable agreement you
 * entered into with Majormode.
 *
 * MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
 * OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
 * TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
 * PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
 * LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
 * OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.
 */

--(defconstant +battery-plug-mode-direct+ 'direct')
--(defconstant +battery-plug-mode-ignition+ 'ignition')


/**
 * The mobile devices that monitor movement and location changes.
 *
 * A mobile device belongs to either an individual user or an
 * organization.  A mobile device cannot be shared between several
 * individual users or organizations.
 *
 * Client applications, installed on a mobile devices, need to be
 * activated in order to use cloud services.  The individual user or an
 * administrator of the organization that manages the mobile device needs
 * to use an administration tool that requests the cloud service to
 * generate an activation code.  This activation code can be displayed
 * as a QR code and scanned by the client application running on the
 * mobile device.  The client application sends the scanned value (the
 * activation code) to the cloud service.  The cloud service activates
 * the client application for this mobile device.  The cloud service
 * generates a security key that it shares with the client application to
 * secure the communication.
 */
CREATE TABLE device (
  /**
   * The identification of the mobile device.
   *
   *
   * @warning It used to be the International Mobile Equipment Identity
   *     (IMEI) of the mobile device.  However, unless mobile application
   *     has been granted privileged permissions (which generally only are
   *     granted to applications preloaded on the device), persistent
   *     device identifiers are guarded behind additional restrictions,
   *     and apps are recommended to use resettable identifiers.
   *
   *
   * @note On Android, this identification is randomly generated when the
   *     user first sets up the device and should remain constant for the
   *     lifetime of the user's device.
   */
  device_id text NOT NULL DEFAULT uuid_generate_v4(),

  /**
   * The hardware serial number of the mobile device. It corresponds to a
   * unique number assigned by the manufacturer to help identifying an
   * individual device.
   *
   *
   * @note: Serial number is not available since Android 10.  This version
   *     changes the permissions for device identifiers so that all device
   *     identifiers are now protected by the `READ_PRIVILEGED_PHONE_STATE`
   *     permission.  This permission is only granted to apps signed with
   *     the platform key and privileged system apps.
   *
   * @note: The serial number is case sensitive.
   */
  serial_number text NULL,

  /**
   * The Media Access Control (MAC) address of the mobile device.  A MAC
   * address is a unique identifier assigned to a network interface for
   * communications at the data link layer of a network segment.
   *
   *
   * @note: MAC address is not available with new version of Android in
   *     2021 (cf. Xiaomi), even with programmatic tricks.
   */
  mac_address macaddr NULL,

  /**
   * The end-user visible name of mobile device model.  This information is
   * immutable.
   */
  device_model text NOT NULL,

  /**
   * The name of the operating system of the mobile device.  This
   * information is immutable.
   */
  os_name text NOT NULL,

  /**
   * The version of the operating system of the mobile device.  This
   * information may be updated from time to time when the operating
   * system of the device is upgraded.
   */
  os_version text NOT NULL,

  /**
   * The identification of the account of the individual user who owns
   * this mobile device, or null if an organization owns this device
   * (cf. {@link device.team_id}).
   */
  account_id uuid NULL,

  /**
   * The identification of the organization that manages this device, or
   * null if an individual user owns this mobile device (cf. {@link
   * device.account_id}).
   */
  team_id uuid NULL,

  /**
   * The identification of the picture that represents this mobile device.
   */
  picture_id uuid NULL,

  /**
   * Indicate whether the mobile device has an internal battery.
   *
   * A device not equipped with an internal battery is indeed less secure
   * as it is immediately shutdown when it is disconnected from the power
   * source of the vehicle the device is mounted on.
   *
   * Device mounted on a motorbike is usually connected to the ignition
   * system of the motorbike, in order not to drain the usual low amperage
   * capacity battery battery of the motorbike when the engine is switched
   * off.  For this reason, such device SHOULD definitively have an
   * internal battery to be still able to communicate with the platform
   * while the motorbike is parked.
   */
  is_battery_present boolean NULL,

  /**
   * Indicate if the internal battery of the mobile device is plugged to
   * a power source.
   */
  is_battery_plugged boolean NULL,

  /**
   * Indicate the method used to plug the battery of the mobile device
   * to the power source of the vehicle this device is mounted on:
   *
   * - `+battery-plug-mode-direct+`:: The battery is directly plugged to the
   *   power source of the vehicle.  Even when the vehicle engine is switched
   *   off, the device is still connected to the power source of the vehicle.
   *   This is the common setup when mounting the device in a vehicle with a
   *   high amperage capacity battery (e.g., automobile, bus, truck, boat).
   *
   * - `+battery-plug-mode-ignition+`: the battery is plugged to the ignition
   *   system of the vehicle.  When the vehicle engine is switched off, the
   *   device is not connected to the power source of the vehicle.  This is
   *   the common setup when mounting the device in a vehicle with low
   *   amperage capacity battery (e.g., motorcycle), in order not to drain
   *   the battery when the vehicle's engine is switched off.
   */
  battery_plug_mode text NULL,

  /**
   * The geographical coordinates of the last known position of the mobile
   * device.
   *
   *
   * @todo: This information should be updated into a cache database (e.g.,
   *     Redis).
   */
  location geometry NULL,

  /**
   * The accuracy in meters of the last known position of the mobile device.
   *
   *
   * @todo: This information should be updated into a cache database (e.g.,
   *     Redis).
   */
  accuracy float NULL,

  /**
   * The horizontal direction of travel, expressed in degrees, of the
   * mobile device when this location has been determined.  It is
   * guaranteed to be in the range `[0.0, 360.0]`.
   *
   *
   * @todo: This information should be updated into a cache database (e.g.,
   *     Redis).
   */
  bearing float NULL,

  /**
   * The speed in meters/second over the ground of the mobile device when
   * this location has been determined.
   *
   *
   * @todo: This information should be updated into a cache database (e.g.,
   *     Redis).
   */
  speed float NULL,

  /**
   * The time when the mobile device determined the information of this fix.
   *
   *
   * @todo: This information should be updated into a cache database (e.g.,
   *     Redis).
   */
  fix_time timestamptz(3) NULL,

  /**
   * The type of the location provider that reported the geographical
   * location such as:
   *
   * - `fused`: The location API in Google Play services that combines
   *   different signals to provide the location information.
   *
   * - `gps`: This provider determines location using satellites.
   *
   * - `network`: This provider determines location based on availability of
   *   cell towers and Wi-Fi access points.  Results are retrieved by means
   *   of a network lookup.
   *
   * - `passive`: A special location provider for receiving locations without
   *   actually initiating a location fix.  This provider can be used to
   *   passively receive location updates when other applications or services
   *   request them without actually requesting the locations yourself.  This
   *   provider will return locations generated by other providers.
   *
   *
   * @todo: This information should be updated into a cache database (e.g.,
   *     Redis).
   */
  provider text NULL,

  /**
   * The time of the last keep-alive (KA) messages sent the mobile device.
   *
   *
   * @todo: This information should be updated into a cache database (e.g.,
   *     Redis).
   */
  keepalive_time timestamptz(3) NULL,

  /**
   * The level in percentage of the mobile device's battery (expressed
   * between `0.0` and `1.1`) when this event occurred.
   *
   *
   * @todo: This information should be updated into a cache database (e.g.,
   *     Redis).
   */
  battery_level float NULL,

  /**
   * The current status of the mobile device:
   *
   * - `deleted`: The device has been banned by an administrator of the
   *   server platform.
   *
   * - `disabled`: The device has been suspended by the individual user who
   *   owns this device or an administrator of the organization that
   *   manages this device.
   *
   * - `enabled`: The device is activated and is expected to operate
   *   properly.
   *
   * - `pending`: The device has not been activated yet.
   */
  object_status text NOT NULL DEFAULT 'pending',

  /**
   * Time when this mobile device has been registered to the platform.
   *
   * @note: This time usually corresponds to the first handshake of the
   *     mobile device with the server platform.
   */
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  /**
   * Time of the most recent modification of one or more attributes of this
   * mobile device.
   */
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);


/**
 * The list of applications that have been once installed on a device,
 * and their respective version.
 *
 *
 * @warning: When the individual user or the organization owning the
 *     mobile device transfer the ownership to another individual user
 *     or organization, the server platform must automatically
 *     deactivate all the client applications running on this device for
 *     security reason.
 */
CREATE TABLE device_app (
  /**
   * The identification of a device.
   */
  device_id text NOT NULL,

  /**
   * The identification of the application that has been installed on the
   * device.
   */
  app_id uuid NOT NULL,

  /**
   * The current version of the application installed on this device.
   */
  app_version text NOT NULL,

  /**
   * The security key generated by the server platform and shared with the
   * application installed on the device to secure the communication.
   *
   *
   * @note: The security key is generated when the application is activated
   *     on this device.
   *
   *
   * @note: A new security key MUST be generated when the ownership of the
   *     device is transferred to another organization.
   */
  security_key text NULL,

  /**
   * The current status of the application on this device.
   *
   * - `enabled`: The application has been enabled by the user or an
   *   administrator of the organization that owns this device.
   *
   * - `deleted`: The application has been deactivated on this mobile
   *   device by the server platform, for instance, when the ownership of
   *   the device has been transferred to another individual user or
   *   organization.
   *
   * - `disabled`: The application has been deactivated by the individual
   *   user or an administrator of the organization that owns this device.
   */
  object_status text NOT NULL,

  /**
   * The time when the application has been registered on this device.
   */
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  /**
   * The time of the most recent update of one or more attributes of the
   * state of this application installed on the device.
   */
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  /**
   * The time when the client application has been activated on the mobile
   * device.
   */
  activation_time timestamptz(3) NULL
);


/**
 * Code generated by the server platform at the request of an individual
 * user or an administrator of an organization to activate client
 * applications running on one or more mobile devices.
 */
CREATE TABLE device_app_activation_request (
  /**
   * A code that a mobile device needs to scan, for instance as a QR code,
   * and to provide back to the server platform in order to be activated.
   */
  activation_code text NOT NULL,

  /**
   * The time when this activation code expires.
   */
  expiration_time timestamptz(3) NOT NULL,

  /**
   * The identification of either the individual user account or either
   * an administrator of the organization on behalf of whom/which this
   * activation has been generated.
   */
  account_id uuid NOT NULL,

  /**
   * The identification of the organization on behalf of which this
   * activation code has been generated.
   */
  team_id uuid NULL,

  /**
   * The identification of the administration application that requested to
   * generate this code for activating a client application running on a
   * mobile device.
   */
  app_id uuid NOT NULL,

  /**
   * The current status of this activation code:
   *
   * - `deleted`: This activation code has expired.
   *
   * - `enabled`: This activation is active.
   */
  object_status text NOT NULL DEFAULT 'enabled',

  /**
   * The time when this activation code has been generated.
   */
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp,

  /**
   * The time of the most recent modification of one or more attributes of
   * this activation code.
   */
  update_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);


/**
 * Event notifying from a change of the state of mobile devices' battery.
 */
CREATE TABLE device_battery_event (
  /**
   * The identification of this event that indicates a state change of the
   * mobile device's battery.
   */
  event_id uuid NOT NULL DEFAULT uuid_generate_v4(),

  /**
   * The identification of this event generated by the client application
   * running on the mobile device that reported this event.
   *
   * This identification is used to detect events that the mobile device
   * would report multiple times.  This happens when network outage occurs
   * after the client application reported successfully a batch of events,
   * but the network connection with the cloud service timed out before the
   * client application had the chance to receive the acknowledgement from
   * the cloud service.  Therefore, the client application reattempts to
   * report one more time these events.
   */
  event_cid text NOT NULL,

  /**
   * The identification of the mobile device which battery state has
   * changed.
  */
  device_id text NOT NULL,

  /**
   * The identification of the client application that collected and sent
   * this event.
  */
  app_id uuid NOT NULL,

  /**
   * The identification of the account of the user logged into the mobile
   * device at the time this event occurred.
   */
  account_id uuid NULL,

  /**
   * Identification of the organization that is responsible for managing
   * this mobile device at the time this event occurred.
   */
  team_id uuid NULL,

  /**
   * The time when the mobile device detected the battery stats change.
   */
  event_time timestamptz(3) NOT NULL,

  /**
   * The type of event that occurred:
   *
   *  - `battery_charging`: The level of the device's battery has increased
   *    significantly;
   *
   *  - `battery_discharging`: The level of the device's battery has decreased
   *    significantly;
   *
   *  - `battery_plugged`: The battery of the device has been plugged to a
   *    power source;
   *
   *  - `battery_unplugged`: The battery of the device has been unplugged from
   *    a power source.
   */
  event_type text NOT NULL,

  /**
   * The level in percentage of the mobile device's battery (expressed
   * between `0.0` and `1.1`) when this event occurred.
   */
  battery_level float NOT NULL,

  /**
   * The geographical coordinates of the position of the mobile device when
   * this event occurred.
   */
  location geometry NULL,

  /**
   * The accuracy in meters of the location.
   */
  accuracy float NULL,

  /**
   * The horizontal direction of travel, expressed in degrees, of the
   * mobile device when this location has been determined.  It is
   * guaranteed to be in the range `[0.0, 360.0]`.
   */
  bearing float NULL,

  /**
   * The speed in meters/second over the ground of the mobile device when
   * this location has been determined.
   */
  speed float NULL,

  /**
   * The time when the mobile device determined the information of this fix.
   */
  fix_time timestamptz(3) NULL,

  /**
   * The type of the location provider that reported the geographical
   * location such as:
   *
   * - `fused`: The location API in Google Play services that combines
   *   different signals to provide the location information.
   *
   * - `gps`: This provider determines location using satellites.
   *
   * - `network`: This provider determines location based on availability of
   *   cell towers and Wi-Fi access points.  Results are retrieved by means
   *   of a network lookup.
   *
   * - `passive`: A special location provider for receiving locations without
   *   actually initiating a location fix.  This provider can be used to
   *   passively receive location updates when other applications or services
   *   request them without actually requesting the locations yourself.  This
   *   provider will return locations generated by other providers.
   */
  provider text NULL,

  /**
   * The time when this battery state change has been stored in the server
   * platform.
   */
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);


/**
 * History of the keep-alive (KA) messages sent by mobile devices to the
 * server platform.
 *
 * A keep-alive message indicates that the link between mobile devices
 * and the server platform is operating, and to notify the platform that
 * the mobile device is still in operation as expected.
 *
 * Keep-alive messages are not queued by the mobile devices.  A keep-
 * alive message is lost if the mobile device was not connected to the
 * Internet, or if a timeout occurred during the transmission of the
 * keep-alive message to the server platform.
 *
 * Keep-alive messages are stored to calculate the quality of service
 * (QoS) of the mobile network operator that the device is connected to.
 * Quality of service (QoS) mechanism controls the performance,
 * reliability and usability of a telecommunications service, and aims
 * to determine the geographical areas where the service coverage is the
 * best.
 *
 *
 * @note: Keep-alive messages don't need the attribute 'client_cid' (an
 *     identification that the client application would have generated)
 *     since these messages are ephemeral.  Each message is sent once,
 *     with no retry if the message would have been lost.
 */
CREATE TABLE device_keepalive_event (
  /**
   * The identification of the keep-alive event.
   */
  event_id uuid NOT NULL DEFAULT uuid_generate_v4(),

  /**
   * The identification of the mobile device that sent the keep-alive
   * message.
   */
  device_id text NOT NULL,

  /**
   * The identification of the client application that sent the keep-alive
   * message.
   */
  app_id uuid NOT NULL,

  /**
   * The identification of the account of the user logged into the mobile
   * device at the time this keep-alive message was sent.
   */
  account_id uuid NULL,

  /**
   * The identification of the organization that is responsible for
   * managing this mobile device at the time this keep-alive message was
   * sent.
   */
  team_id uuid NULL,

  /**
   * The time when the mobile device sent the keep-alive message.
   */
  event_time timestamptz(3) NOT NULL,

  /**
   * The geographical coordinates of the position of the mobile device when
   * this keep-alive message was sent.
   */
  location geometry NULL,

  /**
   * The accuracy in meters of the location.
   */
  accuracy float NULL,

  /**
   * The horizontal direction of travel, expressed in degrees, of the
   * mobile device when this location has been determined.  It is
   * guaranteed to be in the range `[0.0, 360.0]`.
   */
  bearing float NULL,

  /**
   * The speed in meters/second over the ground of the mobile device when
   * this location has been determined.
   */
  speed float NULL,

  /**
   * The time when the mobile device determined the information of this fix.
   */
  fix_time timestamptz(3) NULL,

  /**
   * The type of the location provider that reported the geographical
   * location such as:
   *
   * - `fused`: The location API in Google Play services that combines
   *   different signals to provide the location information.
   *
   * - `gps`: This provider determines location using satellites.
   *
   * - `network`: This provider determines location based on availability of
   *   cell towers and Wi-Fi access points.  Results are retrieved by means
   *   of a network lookup.
   *
   * - `passive`: A special location provider for receiving locations without
   *   actually initiating a location fix.  This provider can be used to
   *   passively receive location updates when other applications or services
   *   request them without actually requesting the locations yourself.  This
   *   provider will return locations generated by other providers.
   */
  provider text NULL,

  /**
   * A string representation of the network connection at the time this
   * geographical location has been determined by the mobile device:
   *
   *     operator:type[:subtype]
   *
   * where:
   *
   * - `operator:string` (required): A Mobile Network Code (MNC) used in
   *   combination with a Mobile Country Code (MCC) (also known as a "MCC/MNC
   *   tuple") to uniquely identify the telephony operator of the mobile
   *   device.
   *
   * - `type:string` (required): A human-readable name that describes the
   *   type of the network that the device is connected to, such as `wifi`,
   *   `mobile`, `unknown`.
   *
   * - `subtype:string` (optional): A human-readable name that describes the
   *   subtype of this network when applicable, such as the radio technology
   *   currently in use on the device for data transmission.  Network of
   *   type `wifi` has no subtype.  Network of type `mobile` can have a
   *   subtype such as `egde`, `gprs`, `hsdpa`, `hspa`, `hspa+`, `umts`, etc.
   */
  network_type text NULL,

  /**
   * The time when this keep-alive message has been stored into the server
   * platform.
   */
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);


/**
 * Location updates that mobile devices reported to the Location Based
 * Service (LBS) platform .
 *
 * A location report generally corresponds to a set of information such
 * as the geographical coordinates of the mobile device at the time its
 * position has been determined, a possible collection of signals that
 * the device has gathered from different sources nearby (Wi-Fi hotspots,
 * cell towers).  This set of information is often called a "fix".
 */
CREATE TABLE device_location_event (
  /**
   * The identification of the location event.
   */
  event_id uuid NOT NULL DEFAULT uuid_generate_v4(),

   /**
   * The identification of this event generated by the client application
   * running on the mobile device that reported this event.
   *
   * This identification is used to detect events that the mobile device
   * would report multiple times.  This happens when network outage occurs
   * after the client application reported successfully a batch of events,
   * but the network connection with the cloud service timed out before the
   * client application had the chance to receive the acknowledgement from
   * the cloud service.  Therefore, the client application reattempts to
   * report one more time these events.
   */
  event_cid text NOT NULL,

  /**
   * The identification of the mobile device that reported this location
   * update.
   */
  device_id text NOT NULL,

  /**
   * The identification of the client application which collected and sent
   * the information of this location update.
   */
  app_id uuid NOT NULL,

  /**
   * The identification of the account of the user logged into the mobile
   * device at the time this location update was reported.
   */
  account_id uuid NULL,

  /**
   * The identification of the organization officially responsible for
   * managing this mobile device at the time this location update was
   * reported.
   */
  team_id uuid NULL,

  /**
   * The time when the mobile device received a notification indicating
   * that the device location has changed.
   */
  event_time timestamptz(3) NOT NULL,

  /**
   * The geographical coordinates of the fix reported by the mobile device.
   */
  location geometry NOT NULL,

  /**
   * The accuracy in meters of the geographical location.
   */
  accuracy float NULL,

  /**
   * The horizontal direction of travel, expressed in degrees, of the
   * mobile device when this location has been determined.  It is
   * guaranteed to be in the range `[0.0, 360.0]`.
   */
  bearing float NULL,

  /**
   * The speed in meters/second over the ground of the mobile device when
   * this location has been determined.
   */
  speed float NULL,

  /**
   * The type of the location provider that reported the geographical
   * location such as:
   *
   * - `fused`: The location API in Google Play services that combines
   *   different signals to provide the location information.
   *
   * - `gps`: This provider determines location using satellites.
   *
   * - `network`: This provider determines location based on availability of
   *   cell towers and Wi-Fi access points.  Results are retrieved by means
   *   of a network lookup.
   *
   * - `passive`: A special location provider for receiving locations without
   *   actually initiating a location fix.  This provider can be used to
   *   passively receive location updates when other applications or services
   *   request them without actually requesting the locations yourself.  This
   *   provider will return locations generated by other providers.
   */
  provider text NULL,

  /**
   * The time when the mobile device determined the information of this
   * fix.
   */
  fix_time timestamptz(3) NOT NULL,

  /**
   * A string representation of the network connection at the time this
   * geographical location has been determined by the mobile device:
   *
   *     MNCMCC:type[:subtype]
   *
   * where:
   *
   * - `MNCMCC:string` (required): A Mobile Network Code (MNC) used in
   *   combination with a Mobile Country Code (MCC) (also known as a "MCC/MNC
   *   tuple") to uniquely identify the telephony operator of the mobile
   *   device.
   *
   * - `type:string` (required): A human-readable name that describes the
   *   type of the network that the device is connected to, such as `wifi`,
   *   `mobile`, `unknown`.
   *
   * - `subtype:string` (optional): A human-readable name that describes the
   *   subtype of this network when applicable.  Network of type `wifi` has
   *   not subtype.  Network of type `mobile` can have a subtype such as
   *   `egde`, `gprs`, `hsdpa`, `hspa`, `hspa+`, `umts`, etc.
   */
  network_type text NULL,

  /**
   * A string representation of the information about the satellites that
   * were used to calculate this geographical location fix:
   *
   *     (azimuth:elevation:PRN:SNR)[, ...]
   *
   * where:
   *
   * - `azimuth:float`: Azimuth of the satellite in degrees.
   *
   * - `elevation:float`: Elevation of the satellite in degrees.
   *
   * - `PRN:integer`: Pseudo-Random Number (PRN) for the satellite.
   *
   * - `SNR:float`: Signal to Noise Ratio (SNR) for the satellite.
   */
  satellites text NULL,

  /**
   * The time when this location update has been stored on the Location
   * Based Service platform.
   */
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp
);


























/**
 * History of the mobile device's activity, such as login and logout,
 * operating system or application version update.
 ou can also see the IP addresses which were used to access your account.


 */
CREATE TABLE device_activity_event (
  /**
   * The identification of the event.
   */
  event_id uuid NOT NULL DEFAULT uuid_generate_v4(),

  /**
   * The identification of the mobile device.
   */
  device_id text NOT NULL,

  /**
   * The identification of the client application installed in the device.
   */
  app_id uuid NOT NULL,

  /**
   * The identification of the account of the user that was using the
   * device when this event occurred.
   */
  account_id uuid NULL,

  /**
   * The identification of the organization that this device belonged to
   * when this event occurred.
   */
  team_id uuid NULL,

  /**
   * The type of event that occurred:
   *
   * - `login_success`: A user successfully signed-in onto the device.
   *
   * - `login_failure`: A user failed to sign-in onto the device.
   *
   * - `logout`: A user signed-out from the device.
   *
   * - `os_update`: The operating system of the device has been updated.
   *
   * - `app_update`: An application installed on the device has been updated.
   */
  event_type text text NOT NULL,

  /**
   * The time when this event occurred.
   */
  event_time timestampz(3) NOT NULL,

  /**
   * The version of the device's operation system at the time this event
   * occurred.
   */
  os_version text NOT NULL

  /**
   * The version of the application that reported this activity.
   */
  app_version text NOT NULL,

  /**
   * The Internet Protocol (IP) address of the mobile device at the time
   * this event occurred.
   */
  ip_address inet NOT NULL,

  /**
   * The geographical coordinates of the position of the mobile device when
   * this event occurred.
   */
  location geometry NULL,

  /**
   * The accuracy in meters of the location.
   */
  accuracy float NULL,

  /**
   * The horizontal direction of travel, expressed in degrees, of the
   * mobile device when this location has been determined.  It is
   * guaranteed to be in the range `[0.0, 360.0]`.
   */
  bearing float NULL,

  /**
   * The speed in meters/second over the ground of the mobile device when
   * this location has been determined.
   */
  speed float NULL,

  /**
   * The time when the mobile device determined the information of this fix.
   */
  fix_time timestamptz(3) NULL,

  /**
   * The type of the location provider that reported the geographical
   * location such as:
   *
   * - `fused`: The location API in Google Play services that combines
   *   different signals to provide the location information.
   *
   * - `gps`: This provider determines location using satellites.
   *
   * - `network`: This provider determines location based on availability of
   *   cell towers and Wi-Fi access points.  Results are retrieved by means
   *   of a network lookup.
   *
   * - `passive`: A special location provider for receiving locations without
   *   actually initiating a location fix.  This provider can be used to
   *   passively receive location updates when other applications or services
   *   request them without actually requesting the locations yourself.  This
   *   provider will return locations generated by other providers.
   */
  provider text NULL,

  /**
   * The time when this event has been stored in the server platform.
   */
  creation_time timestamptz(3) NOT NULL DEFAULT current_timestamp
)
