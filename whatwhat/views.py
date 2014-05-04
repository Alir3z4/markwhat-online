from django.views.generic import TemplateView
from django_markwhat.templatetags.markup import markdown
from whatwhat.forms import WhatForm


class IndexView(TemplateView):
    template_name = "whatwhat/index.html"

    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        form = WhatForm()

        ctx['form'] = form

        if self.request.method == 'POST':
            form = WhatForm(self.request.POST)

            if form.is_valid():
                ctx['markuped_text'] = markdown(form.cleaned_data['text'])

            ctx['form'] = form

        return ctx

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

