# the location of the file with the data to import
DATA_FILE = 'artist/data/artists.json'

# name of the artists index
INDEX_NAME = 'artist-index'

# mapping on th the artist index
ARTIST_MAPPING = {
    "mappings": {
        "artist": {
            "properties": {
                "age": {
                    "type": "long"
                },
                "gender": {
                    "type": "string"
                },
                "location": {
                    "type": "geo_point"
                },
                "rate": {
                    "type": "double"
                },
                "uuid": {
                    "type": "string"
                }
            }
        }
    }
}
