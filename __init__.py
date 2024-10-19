# Imports:
import utils.fetchRestraunt as fetchRestraunt
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from random import shuffle

app = Flask(__name__)
CORS(app)
# Functions:
@app.route('/api/v1/restraunt', methods=['POST'])
def restraunt():
  data = request.json
  url = data.get('url') if data else None
  length = data.get('length') if data else None
  random_order = data.get('random') if data else False

  if url and length and random_order:
    itemarr = fetchRestraunt.getRestraunt(url)
    shuffle(itemarr)
    return jsonify(itemarr[0:length])
  if url and length:
    return jsonify(fetchRestraunt.getRestraunt(url)[0:length])
  if url:
    return jsonify(fetchRestraunt.getRestraunt(url))
  response = make_response(jsonify({'error': 'Please provide a URL'}))
  response.status_code = 400
  return response

if __name__ == '__main__':
    app.run()