import logging

from django.test import Client, TestCase, override_settings

from everbug.middleware import Header


class TestTracer(TestCase):

    @classmethod
    def setUp(cls):
        # Disable notices for expected 404 status
        logging.disable(logging.ERROR)
        cls.client = Client()

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)

    def trace(self, url):
        """
        Makes two requests: target and request of trace data for target request
        We expect REQUEST_ID in the headers of target request, so we generate
        it during the test randomly
        """
        test_id = 'RID_%s' % id(self)
        self.client.get(url, **{Header.REQUEST: test_id})
        return self.client.get(url, **{Header.TRACE: test_id})

    def test_field_context_through_fbv(self):
        response = self.trace('/context/')
        self.assertIn('context', response.content.decode())

    def test_field_context_through_cbv(self):
        response = self.trace('/context_cbv/')
        self.assertIn('context', response.content.decode())

    def test_field_queries_with_single_db(self):
        response = self.trace('/query_single/')
        self.assertIn('queries', response.content.decode())

    def test_field_queries_with_multiply_db(self):
        response = self.trace('/query_multiply/')
        self.assertIn('queries', response.content.decode())

    def test_status_context_through_render(self):
        response = self.trace('/context_render/')
        self.assertEqual(response.status_code, 404)

    def test_status_context_fbv_empty(self):
        response = self.trace('/context_empty/')
        self.assertEqual(response.status_code, 404)

    def test_status_context_cbv_empty(self):
        response = self.trace('/context_empty_cbv/')
        self.assertEqual(response.status_code, 404)

    def test_status_queries_empty(self):
        response = self.trace('/query_no/')
        self.assertEqual(response.status_code, 404)

    def test_if_trace_data_exists(self):
        response = self.client.get('/context/', **{Header.REQUEST: 1})
        self.assertEqual(response[Header.HAS_TRACE], '1')

    def test_if_trace_data_not_exists(self):
        response = self.client.get('/context_empty/', **{Header.REQUEST: 1})
        self.assertEqual(response[Header.HAS_TRACE], '0')

    @override_settings(DEBUG=False)
    def test_headers_if_not_debug(self):
        response = self.client.get('/context/', **{Header.REQUEST: 1})
        self.assertNotIn(Header.HAS_TRACE, response)
