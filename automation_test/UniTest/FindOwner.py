import unittest
from config import config
from server import create_app
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

class SearchByNameIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        with self.client.session_transaction() as sess:
            sess['user_email'] = 'elia.mjdlany@gmail.com'

    def test_find_existing_owner_by_name(self):
        search_owner = 'ruben'
        logger.debug(f"Testing with search owner: {search_owner}")
        response = self.client.post('/search', data={'search': 'ruben', 'selected_search': 'name'})
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ruben', response.data)
        self.assertNotIn(b'No owners found', response.data)
        logger.debug("Test passed. Owner found.")



    def test_find_notexisting_owner_by_name(self):
        search_owner = 'rubben'
        logger.debug(f"Testing with search owner: {search_owner}")
        response = self.client.post('/search', data={'search': 'rubben', 'selected_search': 'name'})
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'rubben', response.data)
        self.assertIn(b'No owners found', response.data)
        logger.debug("Test passed. No owners found.")


if __name__ == '__main__':
    unittest.main()