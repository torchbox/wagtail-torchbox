from django import forms


class ExampleForm(forms.Form):
    """Demonstration of all common Django form fields / widgets"""

    single_line_text = forms.CharField(
        max_length=255, help_text="This is some help text"
    )
    single_line_text_optional = forms.CharField(required=False)
    single_line_text_disabled = forms.CharField(disabled=True)
    multi_line_text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 40})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "autocapitalize": "off"}
        )
    )
    number = forms.IntegerField(widget=forms.NumberInput(attrs={"step": 1}))
    url = forms.URLField(label="URL")
    date = forms.DateField(widget=forms.DateInput(attrs={"placeholder": "DD/MM/YYYY"}))
    datetime = forms.DateTimeField()
    file = forms.FileField(help_text="Please upload a CSV or XLS")
    password = forms.CharField(widget=forms.PasswordInput())
    hidden = forms.CharField(widget=forms.HiddenInput())
    single_checkbox = forms.BooleanField()
    choices = (("one", "One"), ("two", "Two"), ("three", "Three"), ("four", "Four"))
    multiple_checkboxes = forms.MultipleChoiceField(
        choices=choices, widget=forms.CheckboxSelectMultiple()
    )
    select = forms.ChoiceField(choices=choices)
    select_multiple = forms.MultipleChoiceField(choices=choices)
    radio_buttons = forms.ChoiceField(choices=choices, widget=forms.RadioSelect())
