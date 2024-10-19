# Imports:
import utils.fetchRestraunt as fetchRestraunt
from flask import Flask, jsonify, request

app = Flask(__name__)

# Functions:
@app.route('/api/v1/restraunt', methods=['POST'])
def restraunt():
  data = request.json
  url = data.get('url') if data else None
  if url:
    return jsonify(fetchRestraunt.getRestraunt(url))
  return jsonify({'error': 'Please provide a URL'})

if __name__ == '__main__':
    app.run()