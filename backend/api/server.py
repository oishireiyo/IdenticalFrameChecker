import os
import sys
from flask import Flask
from flask import request, make_response, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='', template_folder='')
CORS(app)

# Logging
import logging
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
handler_format = logging.Formatter('%(asctime)s : [%(name)s - %(lineno)d] %(levelname)-8s - %(message)s')
stream_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)

import optparse
parser = optparse.OptionParser()
parser.add_option('--host', dest='host', action='store', default='127.0.0.1', type='string', help='Host name')
parser.add_option('--port', dest='port', action='store', default=5000, type='int', help='Port number')
(options, args) = parser.parse_args()

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src/')
from diff_checker import IdenticalFramesChecker

identicalchecker = IdenticalFramesChecker()

@app.route('/', methods=['GET'])
def index():
  return 'Flask server is running :)'

@app.route('/set_source_name', methods=['POST'])
def set_source_name():
  arguments = request.get_json()
  identicalchecker.set_source_name(source_name=arguments['source_name'])
  response = {'result': True}

  return make_response(jsonify(response))

@app.route('/set_target_name', methods=['POST'])
def set_target_name():
  arguments = request.get_json()
  identicalchecker.set_target_name(target_name=arguments['target_name'])
  response = {'result': True}

  return make_response(jsonify(response))

@app.route('/set_config', methods=['POST'])
def set_config():
  arguments = request.get_json()
  identicalchecker.set_config(config=arguments['config'])
  response = {'result': True}

  return make_response(jsonify(response))

@app.route('/get_video_information', methods=['POST'])
def get_video_information():
  arguments = request.get_json()
  information = identicalchecker.get_video_information(video=arguments['video'])
  response = {'result': True, 'information': information}

  return make_response(jsonify(response))

@app.route('/execute', methods=['GET'])
def execute():
  ijframes = identicalchecker.execute()
  response = {'result': True, 'ijframes': ijframes}

  return make_response(jsonify(response))

if __name__ == '__main__':
  app.debug = True
  app.run(host=options.host, port=options.port)