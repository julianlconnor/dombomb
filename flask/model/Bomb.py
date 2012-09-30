import datetime
import bson

from model.base import DomBombMongo

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
    A_IS_LIVE = 'is_live'
    A_CREATED_AT = 'created_at'
    A_UPDATED_AT = 'updated_at'

    @classmethod
    def setup_indexes(klass):
        from pymongo import ASCENDING
        coll = klass.mdbc()
        coll.ensure_index([(klass.A_IDENTIFIER, ASCENDING),
                           (klass.A_IS_LIVE, ASCENDING)])

    @classmethod
    def create(klass, **kwargs):
        """ Creates a bomb object.
        """
        # flask kwargs are lists to let you pass multiple params if necessary
        doc = {
            klass.A_X : kwargs.get(klass.A_X, [None])[0],
            klass.A_Y : kwargs.get(klass.A_Y, [None])[0],
            klass.A_WIDTH  : kwargs.get(klass.A_WIDTH, [klass.A_DEFAULT_DIMENSION])[0],
            klass.A_HEIGHT : kwargs.get(klass.A_HEIGHT, [klass.A_DEFAULT_DIMENSION])[0],
            klass.A_IDENTIFIER : kwargs.get(klass.A_IDENTIFIER, [None])[0],
            klass.A_CREATED_AT : datetime.datetime.now(),
            klass.A_UPDATED_AT : datetime.datetime.now(),
            klass.A_IS_LIVE : True,
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
            klass.A_IDENTIFIER: kwargs.get(klass.A_IDENTIFIER, [None])[0],
            klass.A_IS_LIVE: True,
        }
        return [a for a in db.find(spec)]

    def disarm(klass, **kwargs):
        """ mark bomb as not live
        """
        db = klass.mdbc()
        spec = {klass.A_OBJECT_ID: bson.ObjectId(kwargs[klass.A_OBJECT_ID])}
        new_vals = {klass.A_IS_LIVE: False,
                    klass.A_UPDATED_AT: datetime.datetime.now(),
        }
        db.update(spec, {'$set': new_vals})
        return True
