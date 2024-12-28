from flask import Flask, jsonify, Response, render_template
from flask_cors import CORS
from db import get_db
from scrape_script import scrape_trending_topics

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/alltrending', methods=['GET'])
def get_trending():
    db = get_db()
    collection = db["trending_topics"]
    trends = list(collection.find({}))
    return jsonify(trends)


@app.route('/api/lasttrending', methods=['GET'])
def get_last_trending():
    db = get_db()
    collection = db["trending_topics"]
    trend = collection.find_one(sort=[('timestamp', -1)])  # Fetch latest trend by timestamp
    return jsonify({
        "message": "Scraping successful",
        "data": trend
    })


@app.route('/api/trending', methods=['GET'])
def scrape_and_save():
    data = scrape_trending_topics()  # Assuming this returns a dictionary with trends
    
    if data:
        # Fetch the last trending data (with the new format)
        last_trending = get_last_trending()
        trend_data = last_trending.get_json() if isinstance(last_trending, Response) else last_trending

        # Prepare the response with updated format
        response = {
            "message": "Scraping successful",
            "data": trend_data['data']  # Extracting 'data' from the response
        }
        return jsonify(response)
    
    return jsonify({"message": "Scraping failed"})

if __name__ == "__main__":
    app.run(debug=True)
