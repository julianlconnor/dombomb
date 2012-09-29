from flask import Flask
import pymongo

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        create_bomb()
    else:
        sweep()

def create_bomb():
    """ Creates a bomb.
        Returns success and coordinates of the bomb.
    """
    pass

def sweep():
    """ Sweeps the provided page for bombs.
        Returns all instances of bombs on that page in JSON.
    """
    pass


if __name__ == "__main__":
    app.run()
