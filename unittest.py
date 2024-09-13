import unittest
from mock import patch
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.execute_query')
    def test_index_no_apps(self, mock_execute_query):
        mock_execute_query.return_value = []
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No apps available', response.data)

    @patch('app.execute_query')
    def test_index_with_apps(self, mock_execute_query):
        mock_execute_query.return_value = [{'id': 1, 'name': 'Test App'}]
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test App', response.data)

    @patch('app.execute_query')
    def test_list_apps(self, mock_execute_query):
        mock_execute_query.return_value = [{'id': 1, 'name': 'Test App'}]
        response = self.app.get('/list')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test App', response.data)

    @patch('app.execute_query')
    def test_delete_app(self, mock_execute_query):
        mock_execute_query.return_value = None
        response = self.app.get('/delete/1')
        self.assertEqual(response.status_code, 302)  # Redirect status code

    @patch('app.execute_query')
    def test_manage_app_add(self, mock_execute_query):
        mock_execute_query.side_effect = [
            None,  # For INSERT INTO apps
            {'id': 1},  # For SELECT id FROM apps
            None,  # For INSERT OR IGNORE INTO tags
            {'id': 1}  # For SELECT id FROM tags
        ]
        response = self.app.post('/app', data={
            'name': 'New App',
            'category': 'Category',
            'description': 'Description',
            'internal_url': 'http://internal.url',
            'external_url': 'http://external.url',
            'extras': '',
            'icon': '',
            'tags': 'tag1,tag2'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after add

    @patch('app.execute_query')
    def test_manage_app_update(self, mock_execute_query):
        mock_execute_query.side_effect = [
            {'name': 'Old App', 'category': 'Old Category'},  # For SELECT * FROM apps
            None,  # For UPDATE apps
            None,  # For DELETE FROM app_tags
            None,  # For INSERT OR IGNORE INTO tags
            {'id': 1}  # For SELECT id FROM tags
        ]
        response = self.app.post('/app/1', data={
            'name': 'Updated App',
            'category': 'Updated Category',
            'description': 'Updated Description',
            'internal_url': 'http://updated.internal.url',
            'external_url': 'http://updated.external.url',
            'extras': '',
            'icon': '',
            'tags': 'tag1,tag2'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after update

if __name__ == '__main__':
    unittest.main()
