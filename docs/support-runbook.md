# Support runbook

This document describes possible ways in which the system may fail or malfunction, with instructions how to handle and recover from these scenarios.

This runbook is supplementary to the [general 24/7 support runbook](https://intranet.torchbox.com/propositions/design-and-build-proposition/delivering-projects/dedicated-support-team/247-support-out-of-hours-runbook/), with details about project-specific actions which may be necessary for troubleshooting and restoring service.

See also our [incident process](https://intranet.torchbox.com/propositions/design-and-build-proposition/delivering-projects/application-support/incident-process/) if you're not already following this.

**Note: Remove the above intranet references if this project will be supported by the client's team, or handed to a third party for support. Consider whether to incorporate any scenarios from the general runbook in these cases.**

## Support resources

- Git repositories:
  - [Project repository]()
  - Include repositories for other dependencies relevant to the runbook
- [Scout APM]()
- Papertrail logs:
  - [Production]()
  - [Staging]()
- [Sentry project]()
- S3 buckets:
  - `project-production`
  - `buckup-project-staging`
- ... Any other resources useful for troubleshooting the site ...

## Scenario X: [Description of overall scenario, e.g. 'Data rejected by AnnoyingService API']

### 1. [Put the most important/likely thing to check first, e.g. 'Is authentication failing?']

- Description of what to check (e.g. 'Does the error response mention "invalid credentials"?')
- Could involve multiple steps (e.g. 'Manually test the credentials with this example cURL command: ...')

**Action if there is an issue with [thing]**

- Description of what to do (e.g. 'Reset the credentials and update the environment variables X and Y with the new details')
- Include technical steps (if fixable), who to raise the issue with (if externally-managed), any specific instructions for communicating with the client

### 2. [Next thing to check if first check wasn't the problem, e.g. 'Is the site posting malformed data?']

...

### 3. [Include as many checks as necessary to cover the possible explanations for the scenario]

...

## Scenario Y: [Another, separate scenario, e.g. 'Search not returning any highlighted results']

...

## Scenario Z: [Include as many different scenarios as necessary for known failure modes of the site]
