import unittest
from server import create_app


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_login_success(self):
        response = self.client.post('/login', data={'email': 'elia.mjdlany@gmail.com', 'password': '12345678'})
        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get('user_email'), 'elia.mjdlany@gmail.com')


    def test_login_invalid_email(self):
        response = self.client.post('/login', data={'email': 'elia_mjdlany@gmail.com', 'password': '12345678'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid Email or password', response.data)


    def test_login_incorrect_password(self):
        response = self.client.post('/login', data={'email': 'elia.mjdlany@gmail.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid Email or password', response.data)


if __name__ == '__main__':
    unittest.main()
