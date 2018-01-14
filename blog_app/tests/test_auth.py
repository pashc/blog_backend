import json
import unittest

from blog_app.tests.test_basic import BasicTest


class AuthTests(BasicTest):
    USER_BASE_URL = '/api/auth/users/'

    def test_valid_user_registration(self):
        # given
        username = 'test_user'
        email = 'bacon@ham.com'
        password = 'pass'

        # when
        result = self.register(username, email, password, password)

        # then
        self.assertEqual(result.status_code, 201)
        result_data = json.loads(result.data)
        self.assertIn(result_data.get('username'), username)
        self.assertIn(result_data.get('email'), email)

    def test_invalid_user_registration_different_passwords(self):
        # when
        result = self.register('user', 'foo@bar.com', 'pass', 'pass2')

        # then
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'The password confirmation failed.', result.data)

    def test_invalid_user_registration_duplicate_email(self):
        # when
        result = self.register('user2', 'foo@bar.com', 'pass', 'pass')

        # then
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'The Username or Email is already in use.', result.data)

    def test_invalid_user_registration_duplicate_user(self):
        # when
        result = self.register('user', 'bar@foo.com', 'pass', 'pass')

        # then
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'The Username or Email is already in use.', result.data)

    def test_get_user_by_id(self):
        # when
        result = self.app.get(self.USER_BASE_URL + str(self.TEST_USER_ID))

        # then
        self.assertEqual(result.status_code, 200)
        result_data = json.loads(result.data)
        self.assertEqual(result_data.get('username'), 'user')
        self.assertEqual(result_data.get('email'), 'foo@bar.com')

    def test_update_user_fails_due_to_already_used_username(self):
        # given
        register_response = self.register(username='UserToUpdate',
                                          email='user@update.com',
                                          password='pass',
                                          confirm='pass')
        self.assertEqual(register_response.status_code, 201)
        user_to_update_id = json.loads(register_response.data).get('id')

        # when
        result = self.app.put(self.USER_BASE_URL + str(user_to_update_id),
                              data=json.dumps(dict(username='user',
                                                   email='updated@user.com',
                                                   password='newPass')),
                              content_type='application/json',
                              headers=self.get_auth_headers())

        # then
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'The Username or Email is already in use.', result.data)

    def test_update_user_fails_due_to_already_used_email(self):
        # given
        register_response = self.register(username='UserToUpdate',
                                          email='user@update.com',
                                          password='pass',
                                          confirm='pass')
        self.assertEqual(register_response.status_code, 201)
        user_to_update_id = json.loads(register_response.data).get('id')

        # when
        result = self.app.put(self.USER_BASE_URL + str(user_to_update_id),
                              data=json.dumps(dict(username='UpdatedUsername',
                                                   email='foo@bar.com',
                                                   password='newPass')),
                              content_type='application/json',
                              headers=self.get_auth_headers())

        # then
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'The Username or Email is already in use.', result.data)

    def test_delete_user(self):
        # given
        register_response = self.register(username='UserToDelete',
                                          email='user@delete.com',
                                          password='pass',
                                          confirm='pass')
        self.assertEqual(register_response.status_code, 201)
        user_to_delete_id = json.loads(register_response.data).get('id')

        # when
        result = self.app.delete(self.USER_BASE_URL + str(user_to_delete_id),
                                 headers=self.get_auth_headers())

        # then
        self.assertEqual(result.status_code, 204)


if __name__ == "__main__":
    unittest.main()
