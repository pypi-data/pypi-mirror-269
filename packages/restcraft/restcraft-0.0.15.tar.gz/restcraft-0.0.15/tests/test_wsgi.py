import json
import unittest

from restcraft.core.routing.response import _HTTP_STATUS_LINES
from test_app.wsgi import application
from webtest import TestApp


class TestWSGI(unittest.TestCase):
    def setUp(self) -> None:
        self.app = application
        self.client = TestApp(application)

    def test_wsgi_method_get(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_int, 200)
        self.assertEqual(resp.status, _HTTP_STATUS_LINES[resp.status_int])

    def test_wsgi_method_post(self):
        resp = self.client.post('/')
        self.assertEqual(resp.status_int, 200)
        self.assertEqual(resp.status, _HTTP_STATUS_LINES[resp.status_int])

    def test_wsgi_method_patch(self):
        resp = self.client.patch('/')
        self.assertEqual(resp.status_int, 200)
        self.assertEqual(resp.status, _HTTP_STATUS_LINES[resp.status_int])

    def test_wsgi_method_put(self):
        resp = self.client.put('/')
        self.assertEqual(resp.status_int, 200)
        self.assertEqual(resp.status, _HTTP_STATUS_LINES[resp.status_int])

    def test_wsgi_method_delete(self):
        resp = self.client.delete('/')
        self.assertEqual(resp.status_int, 200)
        self.assertEqual(resp.status, _HTTP_STATUS_LINES[resp.status_int])

    def test_wsgi_method_head(self):
        resp_head = self.client.head('/')
        resp_get = self.client.get('/')
        self.assertEqual(resp_head.status_int, 200)
        self.assertEqual(
            resp_head.status, _HTTP_STATUS_LINES[resp_head.status_int]
        )
        self.assertEqual(resp_head.body, b'')
        self.assertNotEqual(resp_head.body, resp_get.body)
        self.assertDictEqual(dict(resp_head.headers), dict(resp_get.headers))

    def test_wsgi_not_found(self):
        resp = self.client.get('/not-found', expect_errors=True)
        self.assertEqual(resp.status_int, 404)

    def test_middleware_before_route_early_return(self):
        resp = self.client.get('/before-route-early')
        self.assertEqual(resp.body, b'{"message": "early return"}')

    def test_wsgi_middleware_before_handler_early_return(self):
        resp = self.client.get('/before-handler-early')
        self.assertEqual(resp.body, b'{"message": "early return"}')

    def test_wsgi_middleware_after_handler(self):
        resp = self.client.get('/after-handler')
        self.assertEqual(resp.body, b'{"message": "changed in middleware"}')

    def test_wsgi_handler_return(self):
        resp = self.client.get('/test-handler-return', expect_errors=True)
        self.assertEqual(resp.status_int, 500)
        body = json.loads(resp.body)
        self.assertEqual(body['code'], 'INTERNAL_SERVER_ERROR')
        self.assertEqual(
            body['message'], 'Route handler must return a Response object.'
        )

    def test_wsgi_handler_raise_http_error(self):
        resp = self.client.get('/raise-http-error', expect_errors=True)
        self.assertEqual(resp.status_int, 422)
        body = json.loads(resp.body)
        self.assertEqual(body['code'], 'HTTP_EXCEPTION')
        self.assertEqual(body['message'], 'http-error')

    def test_wsgi_max_body_size(self):
        body = {i: 'a' * 1000 for i in range(1000)}
        resp = self.client.post(
            '/test-max-body',
            body,  # type: ignore
            content_type='application/json',
            expect_errors=True,
        )
        res_body = json.loads(resp.body)
        self.assertEqual(resp.status_int, 413)
        self.assertEqual(res_body['code'], 'BODY_TOO_LARGE')
        self.assertEqual(res_body['message'], 'Request body too large.')
