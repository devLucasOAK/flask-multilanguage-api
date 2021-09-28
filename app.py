from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origins

from posts import posts

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origins
def index():
    lang = request.headers.get("Accepted-Language", "en")[:2]

    p = list(map(lambda post: translate(post, lang), posts))

    return jsonify(p)

@app.route('/posts/<int:id>', methods=['POST'])
@cross_origins
def buy(id): 
    data = request.get_json()

    if('quantity' not in data):
        return jsonify({'message': 'Please, set quantity'}), 400

    quantity = int(data['quantity'])
    post = next(p for p in posts if p['id'] == id)

    if(quantity > post['quantity_left']):
        return jsonify({'message': 'Not Enough'}), 400

    post['quantity_left'] -= quantity

    return jsonify({'message': 'Congratulations'})


def translate(post, lang):

    translation = next(t for t in post['translations'] if t['locale'] == lang)
    
    return {
        'id': post['id'],
        'title': translation['title'],
        'description': translation['description'],
        'image': post['image'],
        'quantityleft': post['quantity_left']
    }


app.run(port=5000)
