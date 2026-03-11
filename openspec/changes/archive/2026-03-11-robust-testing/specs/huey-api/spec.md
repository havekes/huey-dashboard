## ADDED Requirements

### Requirement: Legacy Fallback Support
The system SHALL support legacy list and detail task fetching by falling back to querying the Huey queue directly if no database connection is configured.

#### Scenario: Fallback list query
- **WHEN** the database is not configured and a client requests the task list
- **THEN** the system returns pending and scheduled tasks directly from the Huey queue

#### Scenario: Fallback detail query
- **WHEN** the database is not configured and a client requests details for a specific task ID
- **THEN** the system searches the Huey queue and result store to fulfill the request
