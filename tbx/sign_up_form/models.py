from django import forms
from django.core.mail import EmailMessage
from django.db import models
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.vary import vary_on_headers

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel


class SignUpFormPageBullet(Orderable):
    page = ParentalKey("SignUpFormPage", related_name="bullet_points")
    icon = models.CharField(
        max_length=100,
        choices=(
            ("torchbox/includes/svg/bulb-svg.html", "Light bulb"),
            ("torchbox/includes/svg/pro-svg.html", "Chart"),
            ("torchbox/includes/svg/tick-svg.html", "Tick"),
        ),
    )
    title = models.CharField(max_length=100)
    body = models.TextField()

    panels = [
        FieldPanel("icon"),
        FieldPanel("title"),
        FieldPanel("body"),
    ]


class SignUpFormPageLogo(Orderable):
    page = ParentalKey("SignUpFormPage", related_name="logos")
    logo = models.ForeignKey(
        "torchbox.TorchboxImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        ImageChooserPanel("logo"),
    ]


class SignUpFormPageQuote(Orderable):
    page = ParentalKey("SignUpFormPage", related_name="quotes")
    quote = models.TextField()
    author = models.CharField(max_length=100)
    organisation = models.CharField(max_length=100)

    panels = [
        FieldPanel("quote"),
        FieldPanel("author"),
        FieldPanel("organisation"),
    ]


class SignUpFormPageResponse(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.email


class SignUpFormPageForm(forms.ModelForm):
    class Meta:
        model = SignUpFormPageResponse
        fields = [
            "email",
        ]
        widgets = {
            "email": forms.TextInput(attrs={"placeholder": "Enter your email address"}),
        }


@method_decorator(never_cache, name="serve")
class SignUpFormPage(Page):
    formatted_title = models.CharField(
        max_length=255,
        blank=True,
        help_text="This is the title displayed on the page, not the document "
        "title tag. HTML is permitted. Be careful.",
    )
    intro = RichTextField()
    call_to_action_text = models.CharField(
        max_length=255, help_text="Displayed above the email submission form."
    )
    call_to_action_image = models.ForeignKey(
        "torchbox.TorchboxImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    form_button_text = models.CharField(max_length=255)
    thank_you_text = models.CharField(
        max_length=255, help_text="Displayed on successful form submission."
    )
    email_subject = models.CharField(max_length=100, verbose_name="subject")
    email_body = models.TextField(verbose_name="body")
    email_attachment = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="attachment",
    )
    email_from_address = models.EmailField(
        verbose_name="from address",
        help_text="Anything ending in @torchbox.com is good.",
    )

    sign_up_form_class = SignUpFormPageForm

    content_panels = [
        MultiFieldPanel(
            [FieldPanel("title", classname="title"), FieldPanel("formatted_title")],
            "Title",
        ),
        FieldPanel("intro", classname="full"),
        InlinePanel("bullet_points", label="Bullet points"),
        InlinePanel("logos", label="Logos"),
        InlinePanel("quotes", label="Quotes"),
        MultiFieldPanel(
            [
                FieldPanel("call_to_action_text"),
                ImageChooserPanel("call_to_action_image"),
                FieldPanel("form_button_text"),
                FieldPanel("thank_you_text"),
            ],
            "Form",
        ),
        MultiFieldPanel(
            [
                FieldPanel("email_subject"),
                FieldPanel("email_body"),
                DocumentChooserPanel("email_attachment"),
                FieldPanel("email_from_address"),
            ],
            "Email",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(SignUpFormPage, self).get_context(request, *args, **kwargs)
        context["form"] = self.sign_up_form_class()
        return context

    @vary_on_headers("X-Requested-With")
    def serve(self, request, *args, **kwargs):
        if request.is_ajax() and request.method == "POST":
            form = self.sign_up_form_class(request.POST)

            if form.is_valid():
                form.save()
                self.send_email_response(form.cleaned_data["email"])
                return render(
                    request,
                    "sign_up_form/includes/sign_up_form_page_landing.html",
                    {"page": self, "form": form, "legend": self.call_to_action_text},
                )
            else:
                return render(
                    request,
                    "sign_up_form/includes/sign_up_form_page_form.html",
                    {"page": self, "form": form, "legend": self.call_to_action_text},
                )
        response = super(SignUpFormPage, self).serve(request)
        try:
            del response["cache-control"]
        except KeyError:
            pass
        return response

    def send_email_response(self, to_address):
        email_message = EmailMessage(
            subject=self.email_subject,
            body=self.email_body,
            from_email=self.email_from_address,
            to=[to_address],
        )
        email_message.attach(
            self.email_attachment.file.name.split("/")[-1],
            self.email_attachment.file.read(),
        )
        email_message.send()
