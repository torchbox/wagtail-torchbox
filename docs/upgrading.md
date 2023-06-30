# Upgrading guidelines

This document describes aspects of the system which should be given particular attention when upgrading Wagtail or its dependencies.

## Critical paths

The following areas of functionality are critical paths for the site which don't have full automated tests and should be checked manually.

### 1. Content Management

- **Creating, editing, and publishing pages**: Test the functionality of creating new pages, editing existing content, and publishing changes.
- **Content organization and navigation**: Verify that the site's content hierarchy and navigation structure are maintained correctly after the upgrade.
- **Media management**: Check the uploading, storage, and retrieval of media files, such as images and documents.

### 2. Templates and Styling

- **Front-end templates**: Test the rendering of templates to ensure they display as expected after the upgrade.
- **Styling and CSS**: Check that the site's stylesheets and design elements are correctly applied and maintained.

### 3. Performance and Caching

- **Page loading speed**: Monitor the site's performance and loading times to ensure the upgrade doesn't introduce any significant slowdowns.
- **Caching mechanisms**: Verify that caching mechanisms, such as page caching and database caching, are working correctly.

## Other considerations

As well as testing the critical paths, these areas of functionality should be checked:

- Other places where you know extra maintenance or checks may be necessary
- This could be code which you know should be checked and possibly removed - e.g. because you've patched something until a fix is merged in a subsequent release.
- Any previous fixes which may need to be updated/reapplied on subsequent upgrades
- Technical debt which could be affected by an upgrade.
