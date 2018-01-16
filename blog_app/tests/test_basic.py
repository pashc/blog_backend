import base64
import unittest

from flask import json
from sqlalchemy import text

from blog_app.app import app
from blog_app.database import db


def _restart_db_sequences(engine):
    sequence_sql = '''SELECT sequence_name FROM information_schema.sequences
                        WHERE sequence_schema='public'
                     '''

    for seq in [name for (name,) in db.engine.execute(text(sequence_sql))]:
        try:
            engine.execute(text('ALTER SEQUENCE %s RESTART' % seq))
        except Exception as e:
            print(e)


class BasicTest(unittest.TestCase):
    TEST_USER_ID = -1
    TEST_USER = 'user'
    TEST_USER_EMAIL = 'foo@bar.com'
    TEST_USER_PASS = 'pass'

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/test'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            _restart_db_sequences(db.engine)
            created_test_user_response = self.create_user(self.TEST_USER,
                                                          self.TEST_USER_EMAIL,
                                                          self.TEST_USER_PASS,
                                                          self.TEST_USER_PASS)
            self.TEST_USER_ID = json.loads(created_test_user_response.data).get('id')

        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    ########################
    #### helper methods ####
    ########################

    def get_auth_headers(self):
        return {
            'Authorization': 'Basic ' + base64.b64encode(
                bytes(self.TEST_USER + ":" + self.TEST_USER_PASS, 'ascii')).decode('ascii')
        }

    def create_user(self, username, email, password, confirm):
        return self.app.post(
            '/api/auth/users',
            data=json.dumps(dict(username=username, email=email, password=password, confirm=confirm)),
            content_type='application/json',
            follow_redirects=True
        )
