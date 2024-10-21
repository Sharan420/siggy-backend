# Imports:
import utils.fetchRestraunt as fetchRestraunt
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
from random import shuffle

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Functions:
@app.route('/')
def home():
  response = make_response('hello')
  response.status_code = 200
  return response

@app.route('/api/v1/restraunt', methods=['POST'])
def restraunt():
  data = fetchRestraunt.getRestraunt(request.json.get('url'))
  return jsonify(data)

@app.route('/api/v1/restraunt/menu', methods=['POST'])
def menu():
  data = request.json
  url = data.get('url') if data else None
  length = data.get('length') if data else None
  random_order = data.get('random') if data else False

  if url and length and random_order:
    itemarr = fetchRestraunt.getMenu(url)
    shuffle(itemarr)
    return jsonify(itemarr[0:length])
  if url and length:
    return jsonify(fetchRestraunt.getRestraunt(url)[0:length])
  if url:
    response = make_response(jsonify(fetchRestraunt.getRestraunt(url)))
    response.status_code = 200
    return response
  response = make_response(jsonify({'error': 'Please provide a URL'}))
  response.status_code = 400
  return response

if __name__ == '__main__':
    app.run( port=os.getenv("PORT"), debug=True)
