import factory
from factory.django import DjangoModelFactory
from phonenumber_field.phonenumber import PhoneNumber
from tbx.images.factories import CustomImageFactory
from tbx.people.models import Contact, ContactReason, ContactReasonsList


class ContactFactory(DjangoModelFactory):
    name = factory.Faker("name")
    role = factory.Faker("job")
    image = factory.SubFactory(CustomImageFactory)
    email_address = factory.Faker("email")
    phone_number = factory.LazyAttribute(
        lambda _: PhoneNumber.from_string("+441865123456")
    )

    class Meta:
        model = Contact


class ContactReasonFactory(DjangoModelFactory):
    """
    Factory for generating ContactReason instances.

    Note that this factory cannot be instantiated on its own because ContactReason
    requires a parent ContactReasonsList instance to be associated with.
    Use the ContactReasonsListFactory to create ContactReason instances
    with related parents.
    """

    title = factory.Faker("text", max_nb_chars=20)
    description = factory.Faker("sentence")

    class Meta:
        model = ContactReason


class ContactReasonsListFactory(DjangoModelFactory):
    """
    Factory for generating ContactReasonsList instances along with
    related ContactReason instances.

    *Usage*:

    Create a ContactReasonsList instance without related reasons:

    `contact_reasons_list = ContactReasonsListFactory()`

    Create a ContactReasonsList instance with a specific number of
    related ContactReason instances:

    `contact_reasons_list_with_reasons = ContactReasonsListFactory(reasons=3)`
    """

    name = factory.Faker("text", max_nb_chars=20)
    heading = factory.Faker("text", max_nb_chars=30)

    class Meta:
        model = ContactReasonsList

    @factory.post_generation
    def reasons(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if isinstance(extracted, int):
                ContactReasonFactory.create_batch(extracted, page=self)
            else:
                raise ValueError("The 'reasons' field expects an integer value.")
