# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.6.8] - 2024-04-23
### Added
- Link a device to a user

## [1.6.7] - 2024-04-23
### Changed
- Remove the patch consisting in associating the device to a user

## [1.6.6] - 2023-12-17
### Fixed
- Fix the function `get_device_by_id` to return the missing attribute `device_id`

## [1.6.3] - 2023-01-03
### Changed
- Make public the method `get_device_by_id`

## [1.6.0] - 2023-01-02
### Changed
- Rename the attribute `event_ref` with `event_id`

## [1.5.15] - 2023-01-01
### Added
- Store the last known location of devices in a persistent storage

## [1.5.12] - 2022-12-30
### Changed
- Temporarily deactivate the security token verification

## [1.5.11] - 2022-12-30
### Changed
- Update the body message of the endpoints reporting battery changes and location updates

## [1.5.9] - 2022-12-29
### Added
- Add temporarily the attribute `location: geometry` to the model `device`
- Add temporarily the attribute `accuracy: float` to the model `device`
- Add temporarily the attribute `bearing float: ` to the model `device`
- Add temporarily the attribute `speed: float` to the model `device`
- Add temporarily the attribute `fix_time: timestamptz(3)` to the model `device`
- Add temporarily the attribute `provider: txt` to the model `device`
- Add temporarily the attribute `keepalive_time: timestamptz(3)` to the model `device`
- Add temporarily the attribute `battery_level: float` to the model `device`

## [1.5.8] - 2022-12-23
### Changed
- Migrate to Poetry

## [1.5.7] - 2022-09-28
### Fixed
- Fix API endpoint URLs to send location and battery events

## [1.5.6] - 2022-09-02
### Changed
- Remove the attribute `activation_time` from the model `device`
- Remove the attribute `name` from the model `device`
- Change the attribute `device_id`'s data type of from `uuid` to `string`
- Change MAC address and serial number to optional

## [1.4.3] - 2022-09-02
### Changed
- Does not require passing the MAC address of a device to register
- Fix the name of the parameter `extended_info` with `include_extended_info`

## [1.4.0] - 2022-04-25
### Changed
- Refactor mobile device data model with installed client applications
- Refactor mobile device registration endpoint (handshake)
- Refactor mobile device activation endpoint
- Replace Pipenv with Poetry

## [1.3.5] - 2021-05-24
### Changed
- Enable by default a new tracker device that shake hands for the first time

## [1.3.4] - 2020-12-14
### Changed
- Change method `get_device`'s visibility from `private` to `public`

## [1.3.3] - 2020-11-18
### Changed
- Update the identification of the user currently logged in to the mobile device that sends location updates

## [1.3.2] - 2020-11-18
### Changed
- Update the identification of the user currently logged in to the mobile device that sends a keep-alive message 
 
## [1.3.1] - 2020-11-17
### Changed
- Accept temporarily mobile device not activated to send location updates

## [1.3.0] - 2020-11-17
### Added
- Process keep-alive message from mobile devices
### Changed
- Accept temporarily mobile device not activated to send keep-alive messages

## [1.2.11] - 2020-11-14
### Added
- Register tracker mobile application with its the name of the mobile device's operating system

## [1.2.10] - 2020-11-14
### Added
- Register tracker mobile application with its product name

## [1.2.9] - 2020-11-14
### Changed
- Remove IMEI, IMSI, and ICCID information 
### Added
- Support tracker mobile application handshake with device preregistration
