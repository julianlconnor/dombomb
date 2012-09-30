import settings

class DomBombMongo():
    ##
    ## Database and collection names
    ##
    MONGO_DB_NAME = 'bombs'
    MONGO_COLLECTION_NAME = 'bomb_coll'

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
            connection = Connection(settings.MONGO_HOST, settings.MONGO_PORT)
            klass.MONGO_CONNECTION = connection
        return klass.MONGO_CONNECTION
