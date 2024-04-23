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

/**
 * Ensure that the link between an client application and a device is
 * unique.
 */
CREATE UNIQUE INDEX cst_device_application_unique
  ON device_app (device_id, app_id);

/**
 * Allow fast retrieval of existing activation codes that could be reused
 * for the same individual user or the same organization that has
 * generated them.
 */
CREATE INDEX idx_device_app_activation_request_expiration_time
  ON device_app_activation_request (expiration_time DESC);

/**
 * Allow fast retrieval of battery events, for a given mobile device,
 * filtered or sorted by the time at which the even occurred.
 */
CREATE INDEX idx_device_battery_event_time
  ON device_battery_event (device_id, event_time);

/**
 * Allow fast retrieval of keep-alive messages, for a given mobile device,
 * filtered or sorted by the time at which the event was sent.
 */
CREATE INDEX idx_device_keepalive_event_time
  ON device_keepalive_event (device_id, event_time);

/**
 * Allow fast retrieval of location events, for a given mobile device,
 * filtered or sorted by the time at which the location update event
 * occurred.
 */
CREATE INDEX idx_device_location_event_time
  ON device_location_event (device_id, event_time);


CREATE INDEX idx_device_location_event_cid
  ON device_location_event (event_cid, device_id);

/**
 * Allow fast retrieval of location events, for a given mobile device,
 * filtered or sorted by the time at which the locations have been
 * determined.
 */
CREATE INDEX idx_device_location_event_fix_time
  ON device_location_event (device_id, fix_time);
