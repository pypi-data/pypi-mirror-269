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

ALTER TABLE device
  ADD CONSTRAINT pk_device_id
    PRIMARY KEY (device_id);

ALTER TABLE device
  ADD CONSTRAINT fk_device_account_id
      FOREIGN KEY (account_id)
      REFERENCES account (account_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE device
  ADD CONSTRAINT fk_device_team_id
      FOREIGN KEY (team_id)
      REFERENCES team (team_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;


ALTER TABLE device_app
  ADD CONSTRAINT fk_device_app_id
      FOREIGN KEY (app_id)
      REFERENCES application (app_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE device_app
  ADD CONSTRAINT fk_device_app_device_id
      FOREIGN KEY (device_id)
      REFERENCES device (device_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;


ALTER TABLE device_app_activation_request
  ADD CONSTRAINT fk_device_app_activation_request_app_id
      FOREIGN KEY (app_id)
      REFERENCES application (app_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE device_app_activation_request
  ADD CONSTRAINT fk_device_app_activation_request_account_id
      FOREIGN KEY (account_id)
      REFERENCES account (account_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE device_app_activation_request
  ADD CONSTRAINT fk_device_app_activation_request_team_id
      FOREIGN KEY (team_id)
      REFERENCES team (team_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;


ALTER TABLE device_battery_event
  ADD CONSTRAINT pk_device_battery_event_id
    PRIMARY KEY (event_id);

ALTER TABLE device_battery_event
  ADD CONSTRAINT fk_device_battery_event_account_id
      FOREIGN KEY (account_id)
      REFERENCES account (account_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE device_battery_event
  ADD CONSTRAINT fk_device_battery_event_app_id
      FOREIGN KEY (app_id)
      REFERENCES application (app_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE device_battery_event
  ADD CONSTRAINT fk_device_battery_event_device_id
      FOREIGN KEY (device_id)
      REFERENCES device (device_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE device_battery_event
  ADD CONSTRAINT fk_device_battery_event_team_id
      FOREIGN KEY (team_id)
      REFERENCES team (team_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;


ALTER TABLE device_keepalive_event
  ADD CONSTRAINT pk_device_keepalive_event_id
      PRIMARY KEY (event_id);

ALTER TABLE device_keepalive_event
  ADD CONSTRAINT fk_device_keepalive_event_account_id
      FOREIGN KEY (account_id)
      REFERENCES account (account_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE device_keepalive_event
  ADD CONSTRAINT fk_device_keepalive_event_app_id
      FOREIGN KEY (app_id)
      REFERENCES application (app_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE device_keepalive_event
  ADD CONSTRAINT fk_device_keepalive_event_device_id
      FOREIGN KEY (device_id)
      REFERENCES device (device_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE device_keepalive_event
  ADD CONSTRAINT fk_device_keepalive_event_team_id
      FOREIGN KEY (team_id)
      REFERENCES team (team_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;


ALTER TABLE device_location_event
  ADD CONSTRAINT pk_device_location_event_id
      PRIMARY KEY (event_id);

ALTER TABLE device_location_event
  ADD CONSTRAINT fk_device_location_event_account_id
      FOREIGN KEY (account_id)
      REFERENCES account (account_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE device_location_event
  ADD CONSTRAINT fk_device_location_event_app_id
      FOREIGN KEY (app_id)
      REFERENCES application (app_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE device_location_event
  ADD CONSTRAINT fk_device_location_event_device_id
      FOREIGN KEY (device_id)
      REFERENCES device (device_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;

ALTER TABLE device_location_event
  ADD CONSTRAINT fk_device_location_event_team_id
      FOREIGN KEY (team_id)
      REFERENCES team (team_id)
      ON DELETE CASCADE
      ON UPDATE CASCADE;
