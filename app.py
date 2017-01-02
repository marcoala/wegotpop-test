# -*- coding: utf8 -*-
import os
import datetime
from envparse import Env

from flask import Flask, request, json
from flask.ext.elasticsearch import FlaskElasticsearch

from artist import constants, forms, managers

env = Env()
env.read_envfile()

app = Flask(__name__)
app.config['ELASTICSEARCH_HOST'] = os.environ['BONSAI_URL']
es = FlaskElasticsearch(app, verify_certs=False)


@app.route('/')
def home():
    """ root endpoint, check the status of the service
    """
    data = {
        'message': 'pong',
        'time': datetime.datetime.now()
    }
    return json.jsonify(data)


@app.route('/robots.txt')
def robots():
    """ robots.txt
    """
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res


@app.route('/create_index')
def create_index():
    """ Refresh the index and loads all the artists from file.
        This is a temporary view for testing:
        convert to a command or a task before try to load a big dataset
    """
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


@app.route('/artists', methods=['GET'])
def artists_view():
    """ Main view, retur a list of artist, accepted filters:

        age_max (int)
        age_min (int)
        location_latitude (float)
        location_longitude (float)
        location_radius (float)
        rate_max (float)
        gender (one character, M or F)
    """
    form = forms.ArtistsForm(request.args)
    if form.validate():
        manager = managers.ArtistManager(request.args)
        artists = es.search(index=constants.INDEX_NAME, body={'query': manager.query})
        return json.jsonify(artists)
    else:
        # bad request
        return json.jsonify(form.errors), 400


if __name__ == '__main__':  # pragma: no cover
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
