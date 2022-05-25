from tbx.people import models
from wagtail.admin.forms import WagtailAdminPageForm


class ContactForm(WagtailAdminPageForm):
    def clean_default_contact(self):
        default_contact = self.cleaned_data["default_contact"]

        # If user wants to enable the default contact option
        if default_contact:
            # Make sure only one default contact existing
            models.Contact.objects.filter(default_contact=True).update(
                default_contact=False
            )

        return default_contact
