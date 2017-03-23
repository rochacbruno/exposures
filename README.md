# exposures

Swagger smartAPI for retrieving environmental exposure data.

## Requirements

Requires Python 3.x

Tested on OS X 10.10.5 and Centos 7

## Installation

pip install flasgger

## Running

cd app
python app.py --port <port> --debug

## Test

See the [api documentation](http://localhost:5000/apidocs/index.html) presented by Swagger.

## Notes / TODO

  * The app validates parameters using Flasgger's [validation support](https://github.com/rochacbruno/flasgger#use-the-same-yaml-file-to-validate-your-api-data).
  * Currently investigating if there's a way to use a single, whole Swagger/smartAPI spec instead of breaking into separate operations.
  * Also investigating an issue with support for [swagger definitions](https://github.com/rochacbruno/flasgger/issues/53#issuecomment-288464036).
