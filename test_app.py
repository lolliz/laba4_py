import unittest
import io
import sys
from unittest.mock import patch
from flask import Flask, request, redirect, url_for
from app import check_auth, login, login_post, register

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.add_url_rule('/', 'login', login)
        self.app.add_url_rule('/', 'login_post', login_post, methods=['POST'])
        self.app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])

    @patch('sys.stdout', new=io.StringIO())
    def test_login_post_success(self):
        with self.app.test_client() as client:
            response = client.post('/', data={'username': 'test_user', 'password': 'test_password'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(sys.stdout.getvalue(), 'Вы успешно авторизовались!\n')

    @patch('sys.stdout', new=io.StringIO())
    def test_login_post_failure(self):
        with self.app.test_client() as client:
            response = client.post('/', data={'username': 'wrong_user', 'password': 'wrong_password'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(sys.stdout.getvalue(), 'Неверный логин или пароль.\n')

    @patch('sys.stdout', new=io.StringIO())
    def test_register_success(self):
        with self.app.test_client() as client:
            response = client.post('/register', data={'username': 'test_user', 'password': 'test_password'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(sys.stdout.getvalue(), 'Вы успешно зарегистрировались!\n')

    @patch('sys.stdout', new=io.StringIO())
    def test_register_failure(self):
        with self.app.test_client() as client:
            response = client.post('/register', data={'username': 'test_user', 'password': ''})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(sys.stdout.getvalue(), 'Вы успешно зарегистрировались!\n')

    def test_check_auth_success(self):
        self.assertTrue(check_auth('test_user', 'test_password'))

    def test_check_auth_failure(self):
        self.assertFalse(check_auth('wrong_user', 'wrong_password'))

if __name__ == '__main__':
    unittest.main()