# -*- coding: utf8 -*-
import os
import datetime
from envparse import Env

from flask import Flask, json
from flask.ext.elasticsearch import FlaskElasticsearch

from artist import constants

env = Env()
env.read_envfile()

app = Flask(__name__)
app.config['ELASTICSEARCH_HOST'] = os.environ['BONSAI_URL']
es = FlaskElasticsearch(app, verify_certs=False)


@app.route('/')
def home():
    data = {
        'message': 'pong',
        'time': datetime.datetime.now()
    }
    return json.jsonify(data)


@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res


@app.route('/create_index')
def create_index():
    file_pointer = open(constants.DATA_FILE, 'r')
    data = json.loads(file_pointer.read())
    artists = data['artists']

    # delete the old index (ignore if not found) and create a new one
    es.indices.delete(index=constants.INDEX_NAME, ignore=[400, 404])
    es.indices.create(index=constants.INDEX_NAME, body=constants.ARTIST_MAPPING)

    for artist in artists:
        body = dict()
        body['age'] = artist['age']
        body['gender'] = artist['gender']
        body['rate'] = artist['rate']
        body['uuid'] = artist['uuid']
        body['location'] = artist['latitude'] + ', ' + artist['longitude']
        res = es.index(index=constants.INDEX_NAME, doc_type='artist', body=body)

    es.indices.refresh(index=constants.INDEX_NAME)
    res = es.search(index=constants.INDEX_NAME, body={"query": {"match_all": {}}})

    return json.jsonify(res)


@app.route('/test')
def test_view():
    INDEX_NAME = 'artist-index'
    res = es.search(index=INDEX_NAME, body={
        "query": {
            "bool": {
                "should": [
                    {
                        "range": {
                            "age": {
                                "gte": 0,
                                "lte": 90
                            },
                        }
                    },
                    {
                        "geo_distance": {
                            "distance": "50km",
                            "location": {
                                "lat": "51.5126064",
                                "lon": "-0.1802461"
                            },
                            "weight": 3
                        }
                    }
                ],
                "must": [
                    {
                        "geo_distance": {
                            "distance": "100km",
                            "location": {
                                "lat": "51.5126064",
                                "lon": "-0.1802461"
                            },
                            "weight": 1
                        }
                    }
                ],
                "filter": [
                    {
                        "range": {
                            "rate": {
                                "lte": 50
                            }
                        }
                    },
                    {
                        "match": {
                            "gender": "F",
                        }
                    },
                ]
            }
        }
    })
    return json.jsonify(res)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
