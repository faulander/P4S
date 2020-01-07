from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Setting


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = ('sonarr_url', 'sonarr_apikey', 'sonarr_profile', 'sonarr_autoadd')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save settings'))