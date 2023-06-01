from flask import Flask, jsonify, request
import requests
import uuid
import json
import os

app = Flask(__name__)

key = os.environ.get('API_KEY')
endpoint = os.environ.get('ENDPOINT')
location = "northeurope"

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'GET':
        return jsonify({'message': 'GET request is supported. Use a POST request for translation.'})

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': request.json.get('from_language', 'en'),
        'to': request.json.get('to_languages', [])
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': request.json.get('text', '')
    }]

    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    response_data = response.json()

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
