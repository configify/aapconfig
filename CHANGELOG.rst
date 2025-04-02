## [2.4.0] - 2025-04-02

### Added
- Ability to limit by organization
- Report on more problematic objects

### Changed

### Fixed
- Removal of duplicated objects


## [2.3.2] - 2025-03-28

### Added
- Switch to remove workflow nodes

### Changed

### Fixed
- Survey spec for workflows


## [2.3.1] - 2025-03-27

### Added

### Changed

### Fixed
- Increased inventory group export limit


## [2.3.0] - 2025-03-24

### Added
- Switch to trigger project update

### Changed
- Excluded Control Plane EE from cleanup and export
- Skip encrypted credential fields when applying configurations

### Fixed
- Template survey export
- Message format in notifications export


## [2.2.0] - 2025-03-23

### Added
- Report on duplicate credentials

### Changed
- Consolidated credential variables
- Few minor code improvements
- Excluded controlplane from instance groups export
- Added credential field to all project objects

### Fixed


## [2.1.0] - 2025-03-22

### Added
- Notifications for projects
- Authentication team and org mappings for 2.5
- LDAP and mapping export in 2.5 format

### Changed
- Refactored unused objects playbook

### Fixed
- Webhook credential and inventories for templates and workflows
- Credential owner export for 2.5
- Auditor roles for 2.5
- Documentation on API endpoint for 2.4


## [2.0.0] - 2025-03-12

### Added
- Support for all workflow node types
- Export format selector for roles
- Playbook to export all objects
- Option to trigger synchronization of inventory sources
- Ability to export from AWX 24
- Playbook to convert smart inventories to constructed inventories

### Changed
- Refactored role tasks and playbooks
- Memory and speed optimizations

### Fixed
- Support for oAuth tokens
- Error reporting on project sync
- Collection approval not working for AAP 2.4


## [1.1.0] - 2025-02-28

### Added
- Filter for vars conversion
- Filter for empty fields removal

### Changed

### Fixed
- Host vars format
- Superuses export for 2.5 (https://github.com/configify/aapconfig/issues/3)
- Instance group team role export for 2.4 (https://github.com/configify/aapconfig/issues/5)
- Instance group team tags


## [1.0.0] - 2025-02-24

First release

### Added
- Configuration of Controller
- Configuration of Hub
- Support for AAP 2.5

### Changed

### Fixed
