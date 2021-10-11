from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from posts import posts

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/posts')
@cross_origin()
def index():
    lang = request.headers.get("Accept-Language", "en")[:2]

    p = list(map(lambda post: translate(post, lang), posts))

    return jsonify(p)

@app.route('/posts/<int:id>', methods=['POST'])
@cross_origin()
def buy(id): 
    data = request.get_json()

    if('quantity' not in data):
        return jsonify({'message': 'please_set_quantity'}), 400

    quantity = int(data['quantity'])
    post = next(p for p in posts if p['id'] == id)

    if(quantity > post['quantity_left']):
        return jsonify({'message': 'not_enough'}), 400

    post['quantity_left'] -= quantity

    return jsonify({'message': 'congratulations'})


def translate(post, lang):

    translation = next(t for t in post['translations'] if t['locale'] == lang)
    
    return {
        'id': post['id'],
        'title': translation['title'],
        'description': translation['description'],
        'image': post['image'],
        'quantity_left': post['quantity_left']
    }


app.run(port=5000)
