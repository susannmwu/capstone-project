from unittest import TestCase
from server import app
from model import connect_to_db, db
from flask import session


class FlaskTestsBasic(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        """Stuff to do after each test."""

    def test_index(self):
        result = self.client.get("/")
        self.assertIn(b"Welcome", result.data)

    def test_national_parks_route(self):
        result = self.client.get("/national-parks")
        self.assertIn(b"All National Parks", result.data)

    def test_logout(self):
        """Test logout route."""

        # Start each test with a user ID stored in the session,
        # we want to make sure it gets removed.
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '42'

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn(b'user_id', session)
            self.assertIn(b'Logged Out', result.data)
