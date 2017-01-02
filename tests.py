import unittest
from unittest.mock import patch

from flask import json

import app as myapp


class TestCase(unittest.TestCase):
    """ Generic TestCase class with shared logic for setup and tear down
    """
    def setUp(self):
        myapp.app.config['TESTING'] = True
        self.client = myapp.app.test_client()

    def tearDown(self):
        pass


class TestSimpleViews(TestCase):
    """ Aggregate all test related to very simple view (the ones with little or no logic inside)
    """
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_robots(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)


class TestArtistForm(TestCase):
    """ Tests for the validation of the artist endpoint
    """
    def test_validate_empty_form(self):
        response = self.client.get('/artists')
        self.assertEqual(response.status_code, 200)

    def test_raise_validation_error(self):
        response = self.client.get('/artists?age_min=15')
        self.assertEqual(response.status_code, 400)
        self.assertIn('age_min', json.loads(response.data))


class TestCreateIndex(TestCase):

    @patch('app.es')
    def test_executed_with_no_exception(self, es_mock):
        """ Mock the elasticsearch module and check if the rest fo the logic raise any axception
        """
        self.client.get('/create_index')

    def test_index_creation(self):
        """ Assert that the index is create dwith the right mapping
        """
        pass

    def test_artist_indexing(self):
        """ With a exampel data file assert that each artist is converted in
            the right format
        """
        pass

    def test_response(self):
        """ Assert that after the indexing a refresh is executed and a match_all
            query is executed
        """
        pass


if __name__ == '__main__':
    unittest.main()
