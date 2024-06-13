from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import mysql.connector
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/recommend.js', methods=['GET'])
def get_recommend_js():
    # Fetch data from the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT data FROM recommendations WHERE mid = 1")
    result = cursor.fetchone()
    conn.close()
    
    if result:
        json_data = result['data']
        
        # Fetch the external JavaScript file
        external_js_url = "https://er-recommendation.vercel.app/er-recommend.js"
        response = requests.get(external_js_url)
        if response.status_code == 200:
            external_js_content = response.text
        else:
            return "Failed to fetch external JavaScript file", 500
        
        # Combine json_data and the contents of the external JavaScript file
        js_content = f"""
        window.ERRecommendDefaults = {json_data};
        {external_js_content}
        """
        
        response = make_response(js_content)
        response.mimetype = "application/javascript"
        return response
    else:
        return "No data found", 404

@app.route('/partialconf/<key>', methods=['GET'])
def get_key_value(key):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT data FROM recommendations WHERE mid = 1")
    result = cursor.fetchone()
    conn.close()
    
    if result:
        json_data = json.loads(result['data'])
        if key in json_data:
            return jsonify({key: json_data[key]})
        else:
            return "Key not found", 404
    else:
        return "No data found", 404

@app.route('/partialconf/<key>', methods=['POST'])
def update_key_value(key):
    value = request.json.get('value')
    if value is None:
        return "Value is required", 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT data FROM recommendations WHERE mid = 1")
    result = cursor.fetchone()
    
    if result:
        json_data = json.loads(result['data'])
        json_data[key] = value
        cursor.execute("UPDATE recommendations SET data = %s WHERE mid = 1", (json.dumps(json_data),))
        conn.commit()
        conn.close()
        return "Key updated successfully"
    else:
        return "No data found", 404

if __name__ == '__main__':
    app.run()
