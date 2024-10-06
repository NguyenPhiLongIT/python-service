import os 
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from neo4j import GraphDatabase
import marko
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

URI = "neo4j+s://5ef0fe4c.databases.neo4j.io"
AUTH = ("neo4j", os.getenv("PASSWORD_NEO4J"))
dict = {
    "Concept": "Định nghĩa",
    "Example": "Ví dụ",
    "EnglishName": "Tên tiếng anh",
    "OtherName": "Tên gọi khác",
    "Title": "Tiêu đề",
}
arrPolarityTerm = []
driver = GraphDatabase.driver(URI, auth=AUTH)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route("/graph", methods=["GET"])
def list():
    global dict
    global arrPolarityTerm
    nodes = []
    edges = []
    with driver.session() as session:
        res_result = session.run(
            "MATCH (start)-[r]->(end) \nRETURN id(start) AS source, id(end) AS target"
        )
        for node in res_result:
            new_edge = {
                "source": "node" + str(node["source"]),
                "target": "node" + str(node["target"]),
            }
            edges.append(new_edge)
        nodes_result = session.run("MATCH (n)\nRETURN id(n) AS id, n.Title AS name")
        for node in nodes_result:
            new_node = {"id": node["id"], "name": node["name"]}
            nodes.append(new_node)
        print(len(nodes))
        print(len(edges))
    return jsonify({"nodes": nodes, "edges": edges})

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
        # return jsonify({"response": response.text})
        return Response(response, mimetype='text/xml')
        
    except Exception as e:
        return jsonify({"error": "Request failed"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  
    print(list())
