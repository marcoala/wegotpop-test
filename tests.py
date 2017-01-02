import unittest
from decimal import Decimal as D
from unittest.mock import patch

from flask import json

import app as myapp
from artist import managers, constants


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
    @patch('app.es')
    def test_validate_empty_form(self, es_mock):
        response = self.client.get('/artists')
        self.assertEqual(response.status_code, 200)

    @patch('app.es')
    def test_raise_validation_error(self, es_mock):
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


class TestArtistManager(unittest.TestCase):
    """ Test for the manger, sicne doen't need a flask app use standard TestCase instead of our TestCase
    """

    def test_age_max(self):
        request = {
            'age_max': '30'
        }
        manager = managers.ArtistManager(request)
        query_extended_max_age = manager.query['bool']['must'][0]['range']['age']['lte']
        self.assertEqual(query_extended_max_age, 30 + constants.ARTIST_AGE_EXTENDER)
        query_max_age = manager.query['bool']['should'][0]['range']['age']['lte']
        self.assertEqual(query_max_age, 30)

    def test_age_min(self):
        request = {
            'age_min': '30'
        }
        manager = managers.ArtistManager(request)
        query_extended_min_age = manager.query['bool']['must'][0]['range']['age']['gte']
        self.assertEqual(query_extended_min_age, 30 - constants.ARTIST_AGE_EXTENDER)
        query_min_age = manager.query['bool']['should'][0]['range']['age']['gte']
        self.assertEqual(query_min_age, 30)

    def test_age_range(self):
        request = {
            'age_max': '30',
            'age_min': '30'
        }
        manager = managers.ArtistManager(request)
        query_extended_max_age = manager.query['bool']['must'][0]['range']['age']['lte']
        self.assertEqual(query_extended_max_age, 30 + constants.ARTIST_AGE_EXTENDER)
        query_max_age = manager.query['bool']['should'][0]['range']['age']['lte']
        self.assertEqual(query_max_age, 30)
        query_extended_min_age = manager.query['bool']['must'][0]['range']['age']['gte']
        self.assertEqual(query_extended_min_age, 30 - constants.ARTIST_AGE_EXTENDER)
        query_min_age = manager.query['bool']['should'][0]['range']['age']['gte']
        self.assertEqual(query_min_age, 30)

    def test_location(self):
        request = {
            'location_latitude': '51.5126064',
            'location_longitude': '-0.1802461',
            'location_radius': '100'
        }
        manager = managers.ArtistManager(request)
        query_latitude = manager.query['bool']['should'][0]['geo_distance']['location']['lat']
        query_longitude = manager.query['bool']['should'][0]['geo_distance']['location']['lon']
        query_radius = manager.query['bool']['should'][0]['geo_distance']['distance']
        query_extended_radius = manager.query['bool']['must'][0]['geo_distance']['distance']
        self.assertEqual(query_latitude, '51.5126064')
        self.assertEqual(query_longitude, '-0.1802461')
        self.assertEqual(query_radius, '100km')
        self.assertEqual(query_extended_radius, str(D('100') * constants.ARTIST_DISTANCE_EXTENDER) + 'km')

    def test_rate(self):
        request = {
            'rate_max': '20'
        }
        manager = managers.ArtistManager(request)
        query_rate = manager.query['bool']['filter'][0]['range']['rate']['lte']
        self.assertEqual(query_rate, '20')

    def test_gender(self):
        request = {
            'gender': 'F'
        }
        manager = managers.ArtistManager(request)
        query_gender = manager.query['bool']['filter'][0]['match']['gender']
        self.assertEqual(query_gender, 'F')


if __name__ == '__main__':
    unittest.main()
