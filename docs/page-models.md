# Torchbox.com - Page Models

At the moment we don't have a `BasePage` model that all page models inherit from - they inherit directly from Wagtail's `Page` model. In the future this would be a good thing to refactor.

For now, if creating new page models, make sure they also inherit from the `SocialFields` mixin, so that social image and text fields are added to the 'promote' tab.
