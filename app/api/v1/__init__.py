from flask import Blueprint


api_blueprint = Blueprint(
    "v1",
    __name__,
    url_prefix="/api/v1"
)

from api.v1.departments import *
from api.v1.employees import *
from api.v1.jobs import *
