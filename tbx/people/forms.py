from wagtail.admin.forms import WagtailAdminPageForm

from tbx.people import models


class ContactForm(WagtailAdminPageForm):
    def clean(self):
        cleaned_data = super().clean()

        # Make sure only one contact enabled the default contact option
        default_contact_enabled_count = models.Contact.objects.filter(
            default_contact=True
        ).count()

        # If user wants to enable the default contact option
        if cleaned_data["default_contact"]:
            # If the default contact existed
            if default_contact_enabled_count == 1:
                contact = self.save(commit=False)
                # Only save if user is modifying the default contact
                if not models.Contact.objects.filter(
                    default_contact=True, pk=contact.pk
                ).exists():
                    self.add_error(
                        "default_contact", "There is an existed default contact."
                    )

        return cleaned_data
