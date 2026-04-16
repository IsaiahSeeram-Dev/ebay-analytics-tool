from flask import Flask 
from routes.ebay_routes import ebay_bp


app = Flask (__name__)

app.register_blueprint(ebay_bp)

@app.route('/') 
def home(): 
    return "eBay Tracker Running" 
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


