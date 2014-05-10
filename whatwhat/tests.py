import json
from django.core.urlresolvers import reverse
from django.utils.unittest.case import TestCase
from django.test.client import Client


class TestMarkItWhatView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_parse_markdown(self):
        payload = {
            'parser': 'markdown',
            'what': "**bingo**"
        }

        resp = self.client.post(
            path=reverse('mark_it_what'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_data = json.loads(resp.content)

        self.assertEqual(resp.status_code, 201)
        self.assertIsNotNone(resp_data)
        self.assertIsInstance(resp_data, dict)
        self.assertIn('text', resp_data)
        self.assertEqual(resp_data['text'], "<p><strong>bingo</strong></p>")

    def test_parse_restructuredtext(self):
        payload = {
            'parser': 'restructuredtext',
            'what': "**bingo**"
        }

        resp = self.client.post(
            path=reverse('mark_it_what'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_data = json.loads(resp.content)

        self.assertEqual(resp.status_code, 201)
        self.assertIsNotNone(resp_data)
        self.assertIsInstance(resp_data, dict)
        self.assertIn('text', resp_data)
        self.assertEqual(resp_data['text'], "<p><strong>bingo</strong></p>\n")

    def test_parse_textile(self):
        payload = {
            'parser': 'textile',
            'what': "**bingo**"
        }

        resp = self.client.post(
            path=reverse('mark_it_what'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_data = json.loads(resp.content)

        self.assertEqual(resp.status_code, 201)
        self.assertIsNotNone(resp_data)
        self.assertIsInstance(resp_data, dict)
        self.assertIn('text', resp_data)
        self.assertEqual(resp_data['text'], "\t<p><b>bingo</b></p>")

    def test_invalid_parser(self):
        payload = {
            'parser': 'what?',
            'what': "**bingo**"
        }

        resp = self.client.post(
            path=reverse('mark_it_what'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        resp_data = json.loads(resp.content)

        self.assertEqual(resp.status_code, 404)
        self.assertIsNotNone(resp_data)
        self.assertIsInstance(resp_data, dict)
        self.assertEqual(resp_data['text'], "Invalid parser: what?")