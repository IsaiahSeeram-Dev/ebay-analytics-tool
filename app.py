from flask import Flask 
from routes.ebay_routes import ebay_bp
from database import create_tables

# create Flask app
app = Flask (__name__)

# to register routes (API Endpoints)
app.register_blueprint(ebay_bp)

@app.route('/') 
def home(): 
    return "eBay Tracker Running" 
 

# to create database tables when app starts
create_tables()

# to run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


