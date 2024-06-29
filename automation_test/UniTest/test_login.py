import unittest
from server import create_app
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_login_success(self):
        login_email = 'elia.mjdlany@gmail.com'
        login_pass = '12345678'
        logger.debug(f"Testing login with valid user: {login_email} , {login_pass}")
        response = self.client.post('/login', data={'email': 'elia.mjdlany@gmail.com', 'password': '12345678'})
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get('user_email'), 'elia.mjdlany@gmail.com')
        logger.debug("Test passed. login succeed.")



    def test_login_invalid_email(self):
        login_email = 'elia_mjdlany@gmail.com'
        login_pass = '12345678'
        logger.debug(f"Testing login with invalid email: {login_email} , {login_pass}")
        response = self.client.post('/login', data={'email': 'elia_mjdlany@gmail.com', 'password': '12345678'})
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid Email or password', response.data)
        logger.debug("Test passed. login failed.")



    def test_login_incorrect_password(self):
        login_email = 'elia.mjdlany@gmail.com'
        login_pass = 'wrongpassword'
        logger.debug(f"Testing login with invalid password: {login_email} , {login_pass}")
        response = self.client.post('/login', data={'email': 'elia.mjdlany@gmail.com', 'password': 'wrongpassword'})
        logger.debug(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid Email or password', response.data)
        logger.debug("Test passed. login failed.")



if __name__ == '__main__':
    unittest.main()
