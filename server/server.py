from flask import Flask, request, jsonify, render_template, send_from_directory
import json
# import requests

app = Flask(__name__)
src = "../src"

@app.route('/determine_horizon', methods=['POST'])
def determine_horizon():
    data = request.json

    # implement this 
    # time = get time

    # horizon = determineHorizon(data)
    # sunpath = determineSunPath(time)

    # --------------------------
    # TO-DO
    # - how to display files in browser -> using npm?, flask?
    # --------------------------

    return jsonify({'horizon array': horizon, 'sun path': sunpath})

@app.route('/')
def index():
    return send_from_directory(src, "index.html")

@app.route("/<path:filename>")
def serve_static_file(filename):
    try:
        content_type = None
        if filename.endswith(".css"):
            content_type = "text/css"
        elif filename.endswith(".js"):
            content_type = "application/javascript"

        if content_type:
            print(content_type, " IMPORTED SUCCESSFULY")
            return send_from_directory(src, filename, mimetype=content_type)
        else:
            return "File not found", 404
    except FileNotFoundError:
        return "File not found", 404
    

if __name__ == '__main__':
    app.run(debug=True)