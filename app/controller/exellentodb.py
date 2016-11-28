from flask import jsonify
from app.model.models import *

from exellento import Excellento


json_data = Excellento('svg.xls').json()

print json_data







