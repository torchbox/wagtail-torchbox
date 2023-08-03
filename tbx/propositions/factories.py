import factory
from tbx.people.factories import ContactFactory, ContactReasonsListFactory
from tbx.propositions.models import PropositionPage, SubPropositionPage
from tbx.taxonomy.factories import ServiceFactory
from wagtail_factories import PageFactory


class PropositionPageFactory(PageFactory):
    title = factory.Faker("text", max_nb_chars=20)
    strapline = factory.Faker("sentence")
    service = factory.SubFactory(ServiceFactory)

    class Meta:
        model = PropositionPage


class SubPropositionPageFactory(PageFactory):
    """
    Factory for generating SubPropositionPage instances, with an optional
    related ContactReasonsList instance that has a specified number of
    reasons.

    *Usage*:

    Create a SubPropositionPage instance without a related ContactReasonsList instance:

    `sub_proposition_page = SubPropositionPageFactory()`

    Create a SubPropositionPage instance with a related ContactReasonsList instance
    that has the specified number of reasons:

    `sub_proposition_page = SubPropositionPageFactory(contact_reasons=3)`
    """

    title = factory.Faker("text", max_nb_chars=20)
    strapline = factory.Faker("sentence")
    contact = factory.SubFactory(ContactFactory)

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

    class Meta:
        model = SubPropositionPage
