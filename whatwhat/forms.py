from django import forms
from django.utils.translation import ugettext_lazy as _


class WhatForm(forms.Form):
    MARK_WHAT_MARKDOWN = 0
    MARK_WHAT_TEXTILE = 1
    MARK_WHAT_RST = 2
    MARK_WHAT_HTML2TEXT = 3

    MARK_WHAT_CHOICES = (
        (MARK_WHAT_MARKDOWN, _("Markdown")),
        (MARK_WHAT_TEXTILE, _("Textile")),
        (MARK_WHAT_RST, _("RestructuredText")),
        (MARK_WHAT_HTML2TEXT, _("Html2Text")),
    )

    text = forms.CharField(
        label=_("text"),
        widget=forms.Textarea(),
        min_length=3,
        required=True
    )
    mark_what = forms.ChoiceField(
        label=_("Mark what"),
        choices=MARK_WHAT_CHOICES,
        required=True,
        initial=MARK_WHAT_MARKDOWN,
        widget=forms.RadioSelect()
    )
