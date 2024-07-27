from flask import Flask, request, jsonify, send_from_directory
import os
from chatbot import generate_content, add_user_interest, get_welcome_message

app = Flask(__name__, static_folder='frontend', static_url_path='')


@app.route('/')
def home():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_frontend(path):
    return send_from_directory('frontend', path)

@app.route('/welcome')
def welcome():
    message = get_welcome_message()
    return jsonify({'message': 'Welcome to the AI Content Generator'})

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    user_id = data.get('user_id')
    content_type = data.get('content_type')
    user_input = data.get('user_input')
    num_items = data.get('num_items', 5)  # Default to generating 5 items if not specified
    content_list = generate_content(user_id, content_type, user_input, num_items)
    return jsonify({'content': content_list})

@app.route('/add_interest', methods=['POST'])
def add_interest():
    data = request.json
    user_id = data.get('user_id')
    interest = data.get('interest')
    add_user_interest(user_id, interest)
    return jsonify({'message': 'Interest added successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
