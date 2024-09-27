import os 
from flask import Flask, request, jsonify
from flask_cors import CORS
import marko
import google.generativeai as genai

app = Flask(__name__)
CORS(app)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route('/data', methods=['GET'])
def get_data():
    data = {'message': 'Hello from Python backend!'}
    return jsonify(data)

@app.route('/data', methods=['POST'])
def post_data():
    data = request.json
    print('Received from client:', data)
    return jsonify({'status': 'success', 'received': data})

@app.route("/prompt", methods=["POST"])
def prompt():
    data = request.json
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        model = genai.GenerativeModel("gemini-pro")

        response = model.generate_content(prompt)

        print("Response: ", response)
        return jsonify({"response": response.text})
        
    except Exception as e:
        return jsonify({"error": "Request failed"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  
