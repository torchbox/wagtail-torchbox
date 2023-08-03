import factory
from factory.django import DjangoModelFactory
from tbx.people.factories import ContactFactory, ContactReasonsListFactory
from tbx.taxonomy.models import Service


class ServiceFactory(DjangoModelFactory):
    """
    Factory for generating Service instances, with an optional
    related ContactReasonsList instance that has a specified number of
    reasons.

    *Usage*:

    Create a Service instance without a related ContactReasonsList instance:

    `service_instance = ServiceFactory()`

    Create a Service instance with a related ContactReasonsList instance
    that has the specified number of reasons:

    `service_instance = ServiceFactory(contact_reasons=3)`
    """

    name = factory.Faker("text", max_nb_chars=20)
    slug = factory.Faker("slug")
    description = factory.Faker("paragraph")
    sort_order = factory.Sequence(lambda n: n)
    preferred_contact = factory.SubFactory(ContactFactory)

    class Meta:
        model = Service

    @factory.post_generation
    def contact_reasons(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if isinstance(extracted, int):
                # Create a ContactReasonsList instance with the specified number of reasons
                contact_reasons_list = ContactReasonsListFactory(reasons=extracted)

                # Associate the newly created ContactReasonsList instance with the Service
                self.contact_reasons = contact_reasons_list

            else:
                raise ValueError(
                    "The 'contact_reasons' field expects an integer value."
                )
