from flask import Flask, abort, jsonify, request
import itertools

app = Flask(__name__)

PRODUCTS = {
    1: { 'id': 1, 'name': 'Skello' },
    2: { 'id': 2, 'name': 'Socialive.tv' },
    3: { 'id': 3, 'name': 'Raph'},
}


START_INDEX = len(PRODUCTS) + 1
IDENTIFIER_GENERATOR = itertools.count(START_INDEX)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/v1/products')
def products():
    return jsonify(PRODUCTS)


@app.route('/api/v1/products/<int:product_id>', methods=['GET'])
def product(product_id):
    if product_id in PRODUCTS:
        return jsonify(PRODUCTS[product_id]), 200
    abort(404)


@app.route('/api/v1/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if product_id in PRODUCTS:
        PRODUCTS.pop(product_id, None)
    return '', 204

@app.route('/api/v1/products', methods=['POST'])
def add_product():
    next_value = next(IDENTIFIER_GENERATOR)
    new_product = request.get_json()
    new_product.update({'id': next_value})
    PRODUCTS[next_value] = new_product
    return '', 201

@app.route('/api/v1/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    if product_id in PRODUCTS:
        new_product = request.get_json()
        PRODUCTS[product_id].update(new_product)
        return '', 204
    return '', 422
