from app import *
from app.model.models import *
from app.model.schema import *
from flask import jsonify

@app.errorhandler(404)
def page_not_found(e):
    return 'Error 404: Page not found, Please check ur route well.'

