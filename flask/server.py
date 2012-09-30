import logging
from optparse import OptionParser
from flask import Flask, request, jsonify

import settings
from model.Bomb import Bomb

app = Flask(__name__)


###
### Routers
###
@app.route("/", methods=['GET', 'POST'])
def root():
    fn = create_bomb if request.method == 'POST' else sweep
    return fn(request)

###
### Handler functions
###
def create_bomb(request):
    """ Creates a bomb.
        Returns success and coordinates of the bomb.
    """
    return jsonify({ 'data' : { Bomb.A_OBJECT_ID : Bomb.create(**request.args) } })

def sweep(request):
    """ Sweeps the provided page for bombs.
        Returns all instances of bombs on that page in JSON.
    """
    data = Bomb.sweep(**request.args)
    return jsonify({ 'data': data})


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
