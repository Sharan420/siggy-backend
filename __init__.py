# Imports:
import utils.fetchRestaurant as fetchRestaurant
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
from random import shuffle

load_dotenv()

app = Flask(__name__)
CORS(app)

# Functions:
@app.route('/')
def home():
  response = make_response('hello')
  response.status_code = 200
  return response

@app.route('/api/v1/restaurant', methods=['POST'])
def Restaurant():
  data = fetchRestaurant.getRestaurant(request.json.get('url'))
  if data == {}:
    response = make_response(jsonify({'error': 'Restaurant not found'}))
    response.status_code = 404
    return response
  response = make_response(jsonify(data))
  response.status_code = 200
  return response 

@app.route('/api/v1/restaurant/menu', methods=['POST'])
def menu():
  query_data = request.json

  url = query_data.get('url') if query_data else None
  length = query_data.get('length') if query_data else None
  random_order = query_data.get('random') if query_data else False

  if not length and random_order:
    response = make_response(jsonify({'error': 'Please provide a length'}))
    response.status_code = 400
    return response

  items_arr = fetchRestaurant.getMenu(url)

  if items_arr == []:
    response = make_response(jsonify({'error': 'Menu not found'}))
    response.status_code = 404
    return response

  if url and length and random_order:
    shuffle(items_arr)
    response = make_response(jsonify(items_arr[0:length]))
    response.status_code = 200
    return response
  if url and length:
    response = make_response(jsonify(items_arr[0:length]))
    response.status_code = 200
    return response
  if url:
    response = make_response(jsonify(items_arr))
    response.status_code = 200
    return response
  response = make_response(jsonify({'error': 'Please provide a URL'}))
  response.status_code = 400
  return response

if __name__ == '__main__':
    app.run( host="0.0.0.0", port=os.getenv("PORT"), debug=True)
