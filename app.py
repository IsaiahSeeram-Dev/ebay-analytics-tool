from flask import Flask 

app = Flask (__name__)

@app.route('/') 
def home(): 
    return "eBay Tracker Running" 

@app.route('/analyze')
def analyze():
    return "Analyzing eBay Data..." 


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


