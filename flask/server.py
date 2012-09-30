import logging
import datetime
import simplejson
from optparse import OptionParser
from flask import Flask, request
import bson

import settings
from model.Bomb import Bomb

app = Flask(__name__)


###
### Routers
###
@app.route("/", methods=['GET', 'POST', 'DELETE'])
def root():
    if request.method == 'POST':
        fn = create_bomb
    elif request.method == 'DELETE':
        fn = disarm_bomb
    else:
        fn = sweep
    return fn(request)

###
### Handler functions
###
def create_bomb(request):
    """ Creates a bomb.
        Returns success and coordinates of the bomb.
    """
    bomb_id = str(Bomb.create(**request.args))
    out_json = simplejson.dumps({'data': {Bomb.A_OBJECT_ID: bomb_id}})
    return out_json

def sweep(request):
    """ Sweeps the provided page for bombs.
        Returns all instances of bombs on that page in JSON.
    """
    data = Bomb.sweep(**request.args)
    out_json = simplejson.dumps({'data': data}, default=_coerce_json)
    return out_json

def disarm_bomb(request):
    """ Mark the bomb as used
    """
    Bomb.disarm(**request.args)
    return simplejson.dumps({'data': 'ok'})

def _coerce_json(x):
    """ datetimes to string so they can be encoded as json
    """
    out = x
    if isinstance(x, datetime.datetime):
        out = x.isoformat()
    elif isinstance(x, bson.ObjectId):
        out = str(x)
    return out

###
### Run that shit
###
if __name__ == "__main__":
    """ set environment variable DOMBOMB_ENV=production for production
        otherwise, we use local
    """
    ## command line args
    parser = OptionParser()
    parser.add_option("-p", "--port", dest="port", type="int", help="port chigga", metavar="port", default=5000)
    (options, args) = parser.parse_args()

    if settings.environ == "production":
        app.debug = True  # turn off at some point
        logging.basicConfig(level=logging.INFO)
        host = "0.0.0.0"
    else:
        app.debug = True
        logging.basicConfig(level=logging.DEBUG)
        host = None

    logging.info("Starting server in env: {0} port: {1}".format(settings.environ, options.port))
    app.run(host=host, port=options.port)
