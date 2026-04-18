from flask import Blueprint, request, jsonify
from services.ebay_service import search_items, calculate_profit, analyze_items
from services.ebay_service import get_trending_items
from services.ebay_service import get_smart_trending
from utils.logger import log_info, log_error



ebay_bp = Blueprint('ebay', __name__)

@ebay_bp.route('/search')
def search(): 
    query = request.args.get('query')
    results = search_items(query)
    return jsonify(results)


@ebay_bp.route('/profit')
def profit():
    try:
        buy = float(request.args.get('buy'))
        sell = float(request.args.get('sell'))
        shipping = float(request.args.get('shipping'))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid or missing input"}), 400


@ebay_bp.route('/analyze')
def analyze():
    buy_price = float(request.args.get('buy_price'))

    results = analyze_items(buy_price)
    return jsonify(results)

    result = calculate_profit(buy, sell, shipping)
    return jsonify(result)


@ebay_bp.route('/trending')
def trending():
    results = get_trending_items()
    return jsonify(results)



@ebay_bp.route('/smart')
def smart():
    log_info("Smart endpoint hit")

    try:
        buy_price = request.args.get('buy_price')
        
        # validation
        if buy_price is None:
            return jsonify({
                "error":"buy_price is requried"
            }), 400

        buy_price = float(buy_price)
  
        results = get_smart_trending(buy_price)
        return jsonify(results)
    
    except ValueError:
        return jsonify({
            "error":"buy_price must be a number"
        }), 400 

    except Exception as e:
        log_error(str(e))
        return jsonify({
            "error": "Internal server error"
        }), 500
