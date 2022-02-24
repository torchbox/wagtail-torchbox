# Upgrading guidelines

This document describes aspects of the system which should be given particular attention when upgrading Wagtail or its dependencies.

## Critical paths

The following areas of functionality are critical paths for the site which don't have full automated tests and should be checked manually.

(If this information is managed in a separate document, a link here will suffice.)

### 1. [Summary of critical path, e.g. 'Donations']

[Description of the overall functionality covered]

- Step-by-step instructions for what to test and what the expected behaviour is
- Include details for edge cases as well as the general case
- Break this into separate subsections if there's a lot to cover
- Don't include anything which is already covered by automated testing, unless it's a prerequisite for a manual test

## Other considerations

As well as testing the critical paths, these areas of functionality should be checked:

- Other places where you know extra maintenance or checks may be necessary
- This could be code which you know should be checked and possibly removed - e.g. because you've patched something until a fix is merged in a subsequent release.
- Any previous fixes which may need to be updated/reapplied on subsequent upgrades.
- Technical debt which could be affected by an upgrade.
  - Fixed some NPM vulnerabilities by using the `npm audit fix` command, there are 16 vulnerabilities (13 moderate, 3 high) vulnerabilities required `npm audit fix --force` to be fixed.
