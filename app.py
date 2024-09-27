from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/data', methods=['GET'])
def get_data():
    # Example data to send to the client
    data = {'message': 'Hello from Python backend!'}
    return jsonify(data)

@app.route('/data', methods=['POST'])
def post_data():
    # Get JSON data from client
    data = request.json
    print('Received from client:', data)
    return jsonify({'status': 'success', 'received': data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Make sure the server runs on the correct port
