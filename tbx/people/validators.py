from django.core.exceptions import ValidationError


def DefaultContactValidator(value):
    from tbx.people.models import Contact

    if Contact.objects.filter(default_contact=True).count() < 1:
        raise ValidationError("Only 1 contact can enabled this option.")
