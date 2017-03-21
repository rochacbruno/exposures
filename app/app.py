# -*- coding: utf-8 -*-
"""NCATS Translator Environmental Exposures API.

This application provides an smartAPI compliant endpoint for retrieving
environmental exposure data qualified by temporal and geographic constraints.

It uses Flasgger which provides flexible support for combining Swagger and Flask.
This includes support for validating post parameters according to a Swagger
schema, versioned interfaces, CORS support, and other features.

Todo:
    * Swagger definitions are not yet working. Incorporate.
    * You have to also use ``sphinx.ext.todo`` extension
"""
import os
import traceback
from flask import Flask, jsonify, request
from flask.views import MethodView
from flasgger import Swagger
from flasgger.utils import swag_from, validate, ValidationError

app = Flask(__name__)

""" Define a spec per API version. """
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "Exposures",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
    "specs": [
        {
            "version": "0.0.1",
            "title": "API v1",
            "endpoint": 'v1_spec',
            "description": 'Exposures API - version 1',
            "route": '/v1/spec',
            "rule_filter": lambda rule: rule.endpoint.startswith ('should_be_v1_only')
        }
    ]
}

swagger = Swagger(app)

class Validation(object):
    def __init__(self, message="", status=200):
        self.message = message
        self.status = status

def validate_request (request, schema_id, swagger_spec):
    """ Validate a swagger request against a specified schema object within the
    given Swagger specification. 

    Returns:
        Validation: Returns a validation object [message,status]
    
    """
    result = Validation ()
    try: 
        validate(request.json, schema_id, swagger_spec, root=__file__)
    except ValidationError as e:
        traceback.print_exc ()
        result = Validation ("Validation Error: {0}".format (e), status=400)
    return result

@app.after_request
def allow_origin(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@app.route('/v1/getExposureValue', methods=['POST'], endpoint='should_be_v1_only_getExposureValue')
@swag_from('swagger/getExposureValue.yml')
def get_exposure_value():
    """ Get exposure value. See swagger definition for further details. """
    validation = validate_request (request, 'exposureRequestSchema', 'swagger/getExposureValue.yml')
    if not validation.status == 200:
        return validation.message, validation.status
    return jsonify([
        {
            'start-time' : 0,
            'value'      : 8 + 8,
            'end-time'   : 0
        }
    ])

@app.route('/v1/getExposureScore', methods=['POST'], endpoint='should_be_v1_only_getExposureScore')
@swag_from('swagger/getExposureScore.yml')
def get_exposure_score():
    """ Get exposure score. See swagger spec for further details. """
    validation = validate_request (request, 'exposureScoreRequestSchema', 'swagger/getExposureScore.yml')
    if not validation.status == 200:
        return validation.message, validation.status
    return jsonify([
        {
            'start-time' : 0,
            'value'      : 8 + 8,
            'end-time'   : 0
        }
    ])

if __name__ == "__main__":
    app.run(debug=True)
