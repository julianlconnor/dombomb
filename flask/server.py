from flask import Flask, request, jsonify
from model.Bomb import Bomb
from optparse import OptionParser

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def root():
    fn = create_bomb if request.method == 'POST' else sweep
    return fn(request)

def create_bomb(request):
    """ Creates a bomb.

        Returns success and coordinates of the bomb.
    """
    return jsonify({ 'data' : { Bomb.A_OBJECT_ID : Bomb.create(**request.args) } })

def sweep(request):
    """ Sweeps the provided page for bombs.

        Returns all instances of bombs on that page in JSON.
    """
    return jsonify({ 'data' : Bomb.sweep(**request.args) })

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-p", "--port", dest="port", type="int", help="port chigga", metavar="port", default=5000)

    (options, args) = parser.parse_args()

    app.debug = True
        
    app.run(port=options.port)
