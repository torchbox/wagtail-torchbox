import factory
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
    title = factory.Faker("text", max_nb_chars=20)
    strapline = factory.Faker("sentence")

    class Meta:
        model = SubPropositionPage
