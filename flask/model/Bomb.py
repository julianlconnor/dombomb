import datetime

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
    def create(klass, **kwargs):
        """ Creates a bomb object.
        """
        doc = {
            klass.A_X : kwargs.get(klass.A_X, None),
            klass.A_Y : kwargs.get(klass.A_Y, None),
            klass.A_WIDTH  : kwargs.get(klass.A_WIDTH, klass.A_DEFAULT_DIMENSION),
            klass.A_HEIGHT : kwargs.get(klass.A_HEIGHT, klass.A_DEFAULT_DIMENSION),
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
            klass.A_IDENTIFIER : kwargs.get(klass.A_IDENTIFIER, None)
        }
        return list(db.find(spec))
