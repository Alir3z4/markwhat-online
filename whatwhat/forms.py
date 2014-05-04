from django import forms
from django.utils.translation import ugettext_lazy as _


class WhatForm(forms.Form):
    text = forms.CharField(
        label=_("text"),
        widget=forms.Textarea,
        min_length=3,
        required=True
    )
