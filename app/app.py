
"""NCATS Translator Environmental Exposures API.

This application provides an smartAPI compliant endpoint for retrieving # -*- coding: utf-8 -*-
environmental exposure data qualified by temporal and geographic constraints.

It uses Flasgger which provides flexible support for combining Swagger and Flask.
This includes support for validating post parameters according to a Swagger
schema, versioned interfaces, CORS support, and other features.

Todo:
    * Swagger definitions are not yet working. Incorporate.
    * You have to also use ``sphinx.ext.todo`` extension
"""
import argparse
import calendar
import csv
import logging
# import os
from datetime import datetime

from flask import Flask, jsonify, request
# from flask.views import MethodView

from flasgger import Swagger
from flasgger.utils import swag_from, validate


class LoggingUtil(object):
    @staticmethod
    def init_logging(name):
        FORMAT = '%(asctime)-15s %(filename)s %(funcName)s %(levelname)s: %(message)s'
        logging.basicConfig(format=FORMAT, level=logging.INFO)
        return logging.getLogger(name)


logger = LoggingUtil.init_logging(__file__)

app = Flask(__name__)

""" Define a spec per API version. """
# app.config['SWAGGER'] = {
#     "swagger_version": "2.0",
#     "title": "Exposures",
#     "headers": [
#         ('Access-Control-Allow-Origin', '*'),
#         ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
#         ('Access-Control-Allow-Credentials', "true"),
#     ],
#     "specs": [
#         {
#             "version": "0.0.1",
#             "title": "API v1",
#             "endpoint": 'v1_spec',
#             "description": 'Exposures API - version 1',
#             "route": '/v1/spec',
#             # "rule_filter": lambda rule: rule.endpoint.startswith('should_be_v1_only')
#         }
#     ]
# }

"""
NOTE: Looks like you have only one version by now, so do not need filters
      you can add filters later.

Instead of passing config you can start flasgger with a default data template

* You can even pass all swagger data using the template.

NOTE: IN yaml file and docstring definitions you can only pass:
  tags:
  parameters:
  definitions:
  response:
  produces:
"""

template = {
  "swagger": "2.0",
  "info": {
    "title": "Exposure API",
    "description": "API for environmental exposure models for NIH Data Translator program",
    "contact": {
      "responsibleOrganization": "Data Translator Green Team",
      "responsibleDeveloper": "Data Translator Green Team",
      "email": "help@renci.org",
      "url": "www.renci.org"
    },
    "termsOfService": "None Available",
    "version": "0.0.1"
  },
  #  "host": "exposures.renci.org",
  #   "basePath": "/api",
  "schemes": [
    [
      "http",
      "https"
    ]
  ],
  "operationId": "getExposureValue"
}

swagger = Swagger(app, template=template)


# NOTE: Flasgger does that part, no need to override

# class ValidationError(ValidationError):
#     def __init__(self, message="", status_code=200, payload=None):
#         Exception.__init__(self)
#         self.message = message
#         if status_code is not None:
#             self.status_code = status_code
#         self.payload = payload

#     def to_dict(self):
#         rv = dict(self.payload or ())
#         rv['message'] = self.message
#         return rv


# def validate_request(request, schema_id, swagger_spec):
#     """ Validate a swagger request against a specified schema object within the
#     given Swagger specification.

#     Returns:
#         Validation: Returns a validation object [message,status]

#     """
#     try:
#         validate(request.json, schema_id, swagger_spec, root=__file__)
#     except ValidationError as e:
#         # traceback.print_exc()
#         # raise ValidationError("Validation Error: {0}".format(e), status_code=400)
#         abort(Response(str(e), status=400))


@app.after_request
def allow_origin(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


# no need to override endpoint when you have only one version
# @app.route('/v1/getExposureValue', methods=['POST'], endpoint='should_be_v1_only_getExposureValue')
@app.route('/v1/getExposureValue', methods=['POST'])
@swag_from('swagger/getExposureValue.yml')
def get_exposure_value():
    """ Get exposure value. See swagger definition for further details. """
    validate(request.json, 'exposureValueRequestSchema', 'swagger/getExposureValue.yml')
    logging.info("get_exposure_value({0})".format(request.json))
    return database.get_exposure_value(loc=request.json['loc'],
                                       stime=ExposureUtil.to_timestamp(request.json['stime']),
                                       etime=ExposureUtil.to_timestamp(request.json['etime']),
                                       tres=request.json['tres'],
                                       tstat=request.json['tstat'])


# @app.route('/v1/getExposureScore', methods=['POST'], endpoint='should_be_v1_only_getExposureScore')
@app.route('/v1/getExposureScore', methods=['POST'])
@swag_from('swagger/getExposureScore.yml')
def get_exposure_score():
    """ Get exposure score. See swagger spec for further details. """
    validate(request.json, 'exposureScoreRequestSchema', 'swagger/getExposureScore.yml')
    logging.info("get_exposure_score({0})".format(request.json))
    return database.get_exposure_score(loc=request.json['loc'],
                                       stime=ExposureUtil.to_timestamp(request.json['stime']),
                                       etime=ExposureUtil.to_timestamp(request.json['etime']),
                                       tres=request.json['tres'],
                                       tscore=request.json['tscore'])


# helpers

class ExposureUtil(object):

    @staticmethod
    def to_timestamp(text):
        a_date = datetime.strptime(text, '%Y-%m-%d')
        return calendar.timegm(a_date.timetuple())


''' Test Data '''


class ExposuresDBStub (object):
    def __init__(self):
        self.data = []
        # with open('../data/sample_cmaq_output_updated.csv', 'r') as csvfile:
        #     reader = csv.DictReader (csvfile)
        #     for row in reader:
        #         # ID,Lat,Lon,Col,Row,Date,O3_ppb,PM25_Primary_ugm3,PM25_Secondary_ugm3
        #         # Raleigh,35.7795897,-78.6381787,122,50,2010-01-01 00:00:00,4.67542219161987,10.2763252258301,10.2763252258301
        #         dt = datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S')
        #         t = calendar.timegm(dt.timetuple())
        #         self.data.append ([
        #             float(row['Lat']),
        #             float(row['Lon']),
        #             t,
        #             row['PM25_Primary_ugm3'],
        #             row['PM25_Secondary_ugm3']
        #         ])

    def get_exposure_value(self, loc, stime, etime, tres, tstat):
        result = {"exposure": -1}
        lat, lon = map(lambda t: float(t), loc.split(',')[0: 2])
        for row in self.data:
            if row[0] == lat and row[1] == lon:
                result = {"exposure": row[3]}
                break
        return jsonify(result)

    def get_exposure_score(self, loc, stime, etime, tres, tscore):
        return self.get_exposure_value(loc, stime, etime, tres, tscore)


class DatabaseFactory (object):
    def __init__(self, mode="test"):
        self.mode = mode

    def create_db(self):
        return ExposuresDBStub()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode",  help="Database mode [test|prod]", default="test")
    parser.add_argument("--port",  help="Port to serve on", default=5000)
    parser.add_argument("--debug", help="Activate debug mode", action='store_true')
    args = parser.parse_args()

    database_factory = DatabaseFactory(mode=args.mode)
    database = database_factory.create_db()

    app.run(
        port=int(args.port),
        debug=args.debug,
        host='0.0.0.0'
    )
