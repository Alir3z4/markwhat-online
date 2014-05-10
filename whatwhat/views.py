import json
import logging
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View
from django_markwhat.templatetags.markup import markdown, textile, restructuredtext


class IndexView(TemplateView):
    template_name = "whatwhat/index.html"


class MarkItWhatView(View):
    parsers = {
        'textile': textile,
        'markdown': markdown,
        'restructuredtext': restructuredtext
    }
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(MarkItWhatView, self).dispatch(*args, **kwargs)

    def validate_request_data(self, request):
        data = None
        # import ipdb;ipdb.set_trace()
        try:
            data = json.loads(request.body)
        except Exception as exc:
            logging.error("Invalid request: {0}".format(exc))
            raise Http404

        return data

    def validate_parser(self, parser_name):
        """
        :type parser_name: basestring

        :rtype: bool
        """
        if parser_name not in self.parsers:
            return False

        return True


    def get_parser_class(self, parser_name):
        """
        :type parser_name: basestring
        """
        return self.parsers[parser_name]

    def post(self, request, *args, **kwargs):
        data = self.validate_request_data(request)
        parser_name = data['parser']
        if not self.validate_parser(parser_name):
            return HttpResponseNotFound(
                json.dumps({
                    'text': 'Invalid parser: {0}'.format(parser_name)
                })
            )

        parser = self.get_parser_class(parser_name)
        payload = {
            'text': parser(data['what'])
        }

        return HttpResponse(
            status=201,
            content_type='application/json',
            content=json.dumps(payload)
        )
