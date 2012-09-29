from flask import Flask, request, jsonify
from model.Bomb import Bomb

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def root():
    fn = create_bomb if request.method == 'POST' else sweep
    return fn(request)

def create_bomb(request):
    """ Creates a bomb.

        Returns success and coordinates of the bomb.
    """
    return jsonify({ 'data' : { Bomb.A_OBJECT_ID : Bomb.create(**request.form) } })

def sweep(request):
    """ Sweeps the provided page for bombs.

        Returns all instances of bombs on that page in JSON.
    """
    return jsonify({ 'data' : Bomb.sweep(**request.form) })


if __name__ == "__main__":
    app.debug = True
    app.run()
