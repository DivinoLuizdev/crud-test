from flask import Blueprint, jsonify, request
from app.services.product_service import ProductService

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return jsonify({"message": "API de Produtos rodando!"})

# CRUD existente
@bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product = ProductService.create_product(data)
    return jsonify(product.to_dict()), 201

@bp.route('/products', methods=['GET'])
def list_products():
    products = ProductService.get_all_products()
    return jsonify([p.to_dict() for p in products])

@bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = ProductService.get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Produto não encontrado"}), 404
    return jsonify(product.to_dict())

@bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = ProductService.update_product(product_id, data)
    if not product:
        return jsonify({"error": "Produto não encontrado"}), 404
    return jsonify(product.to_dict())

@bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = ProductService.delete_product(product_id)
    if not product:
        return jsonify({"error": "Produto não encontrado"}), 404
    return jsonify({"message": f"Produto {product_id} excluído com sucesso!"})

# 🔹 BUSCAS
@bp.route('/products/search', methods=['GET'])
def search_products():
    name = request.args.get('name')
    category = request.args.get('category')
    products = ProductService.search_products(name, category)
    return jsonify([p.to_dict() for p in products])

@bp.route('/products/category/<string:category>', methods=['GET'])
def products_by_category(category):
    products = ProductService.get_products_by_category(category)
    return jsonify([p.to_dict() for p in products])

@bp.route('/products/image', methods=['GET'])
def products_with_image():
    has_image = request.args.get('has_image', 'true').lower() == 'true'
    products = ProductService.get_products_with_image(has_image)
    return jsonify([p.to_dict() for p in products])

 
@bp.route('/products/import', methods=['POST'])
def import_products():
    data = request.get_json()
    api_url = data.get("api_url", "https://fakestoreapi.com/products")
    result, status = ProductService.import_products_from_api(api_url)
    return jsonify(result), status

