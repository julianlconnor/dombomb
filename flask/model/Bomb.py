import datetime
import pymongo
from pymongo import DESCENDING

class Bomb():
    ##
    ## Attributes
    ##
    A_OBJECT_ID = "_id"

    A_X = 'x'
    A_Y = 'y'

    A_DEFAULT_DIMENSION = '50'

    A_WIDTH      = 'width'
    A_HEIGHT     = 'height'
    A_IDENTIFIER = 'identifier'

    A_CREATED_AT = 'created_at'
    A_UPDATED_AT = 'updated_at'

    ##
    ## Database and collection names
    ##
    MONGO_DB_NAME = 'bombs'
    MONGO_COLLECTION_NAME = 'bomb_coll'

    @classmethod
    def setup_mongo_indexes(klass):
        db = klass.mdbc()
        db.ensure_index([(klass.A_IDENTIFIER, DESCENDING) ])

    @classmethod
    def mdbc(klass):
        """ Memoized pymongo connection.
        """
        
        if not getattr(klass, 'MONGO_COLL_POINTER', None):
            connection = pymongo.connection()
            db = connection[klass.MONGO_DB_NAME]
            klass.MONGO_COLL_POINTER = db[klass.MONGO_COLLECTION_NAME]

        return klass.MONGO_COLL_POINTER

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


