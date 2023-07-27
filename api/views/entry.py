# -*- coding:utf-8 -*-

import os

from flask import Blueprint
from flask_restful import Api

from api.resource import register_resources

HERE = os.path.abspath(os.path.dirname(__file__))

# hello api
blueprint_test_v01 = Blueprint('api', __name__, url_prefix='/api/v0.1')
rest = Api(blueprint_test_v01)
register_resources(os.path.join(HERE, "your_app"), rest)  # TODO: replace your_app
