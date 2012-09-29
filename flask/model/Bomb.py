import os
import datetime

class DomBombMongo():
    ##
    ## Database and collection names
    ##
    MONGO_DB_NAME = 'bombs'
    MONGO_COLLECTION_NAME = 'bomb_coll'
    MONGO_HOST = os.environ.get('MONGO_HOST');
    MONGO_PORT = os.environ.get('MONGO_PORT');

    @classmethod
    def setup_mongo_indexes(klass):
        from pymongo import DESCENDING

        db = klass.mdbc()
        db.ensure_index([(klass.A_IDENTIFIER, DESCENDING) ])

    @classmethod
    def mdbc(klass):
        """ Memoized pymongo connection.
        """
        
        if not getattr(klass, 'MONGO_COLL_POINTER', None):
            connection = klass.mongo_connection()
            db = connection[klass.MONGO_DB_NAME]
            klass.MONGO_COLL_POINTER = db[klass.MONGO_COLLECTION_NAME]

        return klass.MONGO_COLL_POINTER

    @classmethod
    def mongo_connection(klass):
        """ returns a pointer to the DB"""

        if not getattr(klass, 'MONGO_CONNECTION', None):

            from pymongo.connection import Connection
            connection = Connection(klass.MONGO_HOST, klass.MONGO_PORT)
            klass.MONGO_CONNECTION = connection

        return klass.MONGO_CONNECTION

class Bomb(DomBombMongo):
    ##
    ## Attributes
    ##
    A_OBJECT_ID = "_id"

    A_X = 'x'
    A_Y = 'y'

    A_WIDTH      = 'width'
    A_HEIGHT     = 'height'

    A_DEFAULT_DIMENSION = '50'

    A_IDENTIFIER = 'identifier'

    A_CREATED_AT = 'created_at'
    A_UPDATED_AT = 'updated_at'

    @classmethod
    def create(klass, **kwargs):
        """ Creates a bomb object.
        """
        doc = {
            klass.A_X : kwargs.get(klass.A_X, None),
            klass.A_Y : kwargs.get(klass.A_Y, None),
            klass.A_WIDTH  : kwargs.get(klass.A_WIDTH, klass.A_DEFAULT_DIMENSION),
            klass.A_HEIGHT : kwargs.get(klass.A_HEIGHT, klass.A_DEFAULT_DIMENSION),
            klass.A_CREATED_AT : datetime.datetime.now(),
            klass.A_UPDATED_AT : datetime.datetime.now()
        }

        klass.mdbc().insert(doc)
        id = str(doc.get(klass.A_OBJECT_ID))

        return id

    @classmethod
    def sweep(klass, **kwargs):
        """ Returns the results for the provided identifier.
        """
        db = klass.mdbc()

        spec = {
            klass.A_IDENTIFIER : kwargs.get(klass.A_IDENTIFIER, None)
        }

        return db.find(spec)

