from flask import Flask, request, jsonify, render_template
from chatbot import generate_content, add_user_interest

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    user_id = data.get('user_id')
    content_type = data.get('content_type')
    user_input = data.get('user_input')
    content = generate_content(user_id, content_type, user_input)
    return jsonify({'content': content})

@app.route('/add_interest', methods=['POST'])
def add_interest():
    data = request.json
    user_id = data.get('user_id')
    interest = data.get('interest')
    add_user_interest(user_id, interest)
    return jsonify({'message': 'Interest added successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
