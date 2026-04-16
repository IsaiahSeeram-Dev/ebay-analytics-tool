from flask import Blueprint, request, jsonify
from services.ebay_service import search_items

ebay_bp = Blueprint('ebay', __name__)

@ebay_bp.route('/search')
def search(): 
    query = request.args.get('query')
    results = search_items(query)
    return jsonify(results)

