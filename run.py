from app import *
from app.api.get import *
from app.api.post import *
from app.api.put import *


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
