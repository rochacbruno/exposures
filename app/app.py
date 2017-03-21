import os
import traceback
from flask import Flask, jsonify, request
from flask.views import MethodView
from flasgger import Swagger
from flasgger.utils import swag_from, validate, ValidationError

app = Flask(__name__)


# config your API specs
# you can define multiple specs in the case your api has multiple versions
# ommit configs to get the default (all views exposed in /spec url)
# rule_filter is a callable that receives "Rule" object and
#   returns a boolean to filter in only desired views

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
            "title": "Api v1",
            "endpoint": 'v1_spec',
            "description": 'Exposures API - version 1',
            "route": '/v1/spec',
            # rule_filter is optional
            # it is a callable to filter the views to extract
            "rule_filter": lambda rule: rule.endpoint.startswith(
                'should_be_v1_only'
            )
        }
    ]
}

swagger = Swagger(app)

@app.after_request
def allow_origin(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://example.com'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@app.route('/v1/getExposureValue', methods=['POST'], endpoint='should_be_v1_only_getExposureValue')
@swag_from('swagger/getExposureValue.yml')
def get_exposure_value():
    print (request.json)
    try: 
        validate(request.json, 'exposureRequestSchema', 'swagger/getExposureValue.yml', root=__file__)
    except ValidationError as e:
        traceback.print_exc ()
        print (str(e))
        return "Validation Error: %s" % e, 400
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
    print (request.json)
    try: 
        validate(request.json, 'exposureScoreRequestSchema', 'swagger/getExposureScore.yml', root=__file__)
    except ValidationError as e:
        traceback.print_exc ()
        print (str(e))
        return "Validation Error: %s" % e, 400
    return jsonify([
        {
            'start-time' : 0,
            'value'      : 8 + 8,
            'end-time'   : 0
        }
    ])

if __name__ == "__main__":
    app.run(debug=True)
