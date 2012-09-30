""" Settings file

    Set DOMBOMB_ENV=production in shell for production, otherwise it defaults
    to local
"""

import os

environ = "production" if os.environ.get('DOMBOMB_ENV') == "production" else "local"

## Mongodb stuff
if environ == "production":
    MONGO_HOST = "localhost"
    MONGO_PORT = 27017
else:
    MONGO_HOST = "localhost"
    MONGO_PORT = 27017
