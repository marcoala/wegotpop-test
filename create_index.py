from envparse import Env

from flask import Flask, json
from flask.ext.elasticsearch import FlaskElasticsearch

env = Env()
env.read_envfile()

app = Flask(__name__)
app.config['ELASTICSEARCH_HOST'] = os.environ['BONSAI_URL']
es = FlaskElasticsearch(app)

DATA_FILE = 'data/artists.json'

file_pointer = open(DATA_FILE, 'r')
data = json.loads(file_pointer.read())
artists = data['artists']
