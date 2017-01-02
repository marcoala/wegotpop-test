from decimal import Decimal as D
from artist import constants


class ArtistManager(object):
    """ create an ElasticSearch query form a series of filter
    """
    def __init__(self, filter_set):
        should = []
        must = []
        filter_query = []
        if 'age_max' in filter_set or 'age_min' in filter_set:
            age_range = {"range": {"age": {}}}
            extended_age_range = {"range": {"age": {}}}
            if 'age_max' in filter_set:
                age_max = int(filter_set['age_max'])
                age_range['range']['age']['lte'] = age_max
                extended_age_range['range']['age']['lte'] = age_max + constants.ARTIST_AGE_EXTENDER
            if 'age_min' in filter_set:
                age_min = int(filter_set['age_min'])
                age_range['range']['age']['gte'] = age_min
                extended_age_range['range']['age']['gte'] = age_min - constants.ARTIST_AGE_EXTENDER
            must.append(extended_age_range)
            should.append(age_range)

        if 'location_latitude' in filter_set and \
           'location_longitude' in filter_set and \
           'location_radius' in filter_set:
            radius = D(filter_set['location_radius'])
            location = {
                "lat": filter_set['location_latitude'],
                "lon": filter_set['location_longitude']
            }
            distance = str(radius) + 'km'
            extended_distance = str(radius * constants.ARTIST_DISTANCE_EXTENDER) + 'km'
            must.append({"geo_distance": {"distance": extended_distance, "location": location}})
            should.append({"geo_distance": {"distance": distance, "location": location}})

        if 'rate_max' in filter_set:
            rate_filter = {"range": {"rate": {"lte": filter_set['rate_max']}}}
            filter_query.append(rate_filter)

        if 'gender' in filter_set:
            gender_filter = {"match": {"gender": filter_set['gender']}}
            filter_query.append(gender_filter)

        self.query = {'bool': {'should': should, 'must': must, 'filter': filter_query}}
