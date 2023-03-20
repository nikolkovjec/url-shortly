import unittest
import json
from app import app


class TestUrlShortener(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_shorten_url(self):
        url = {'url': 'https://www.example.com'}
        response = self.app.post('/shorten', json=url)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['short_url'])

    def test_expand_url(self):
        url = {'url': 'https://www.example.com'}
        response = self.app.post('/shorten', json=url)
        short_url = json.loads(response.get_data(as_text=True))['short_url']
        response = self.app.get(f'/{short_url}')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response.headers['Location'], 'https://www.example.com')

    def test_shorten_url_duplicate(self):
        url = {'url': 'https://www.example.com'}
        response1 = self.app.post('/shorten', json=url)
        response2 = self.app.post('/shorten', json=url)
        data1 = json.loads(response1.get_data(as_text=True))
        data2 = json.loads(response2.get_data(as_text=True))
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(data1['short_url'], data2['short_url'])

    def test_expand_url_not_found(self):
        response = self.app.get('/not_a_short_url')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['error'])


if __name__ == '__main__':
    unittest.main()
