from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import mysql.connector
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})

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

# @app.route('/partialconf/<key>', methods=['GET'])
# def get_key_value(key):
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT data FROM recommendations WHERE mid = 1")
#     result = cursor.fetchone()
#     conn.close()
    
#     if result:
#         json_data = json.loads(result['data'])
#         if key in json_data:
#             return jsonify({key: json_data[key]})
#         else:
#             return "Key not found", 404
#     else:
#         return "No data found", 404

# @app.route('/partialconf/<key>', methods=['POST'])
# def update_key_value(key):
#     value = request.json.get('value')
#     if value is None:
#         return "Value is required", 400
    
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT data FROM recommendations WHERE mid = 1")
#     result = cursor.fetchone()
    
#     if result:
#         json_data = json.loads(result['data'])
#         json_data[key] = value
#         cursor.execute("UPDATE recommendations SET data = %s WHERE mid = 1", (json.dumps(json_data),))
#         conn.commit()
#         conn.close()
#         return "Key updated successfully"
#     else:
#         return "No data found", 404

@app.route('/partialconf', methods=['POST'])
def post_partial_conf():
    new_config = request.json
    if not new_config:
        return jsonify({"error": "Invalid input"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT data FROM recommendations WHERE mid = 1")
    result = cursor.fetchone()
    
    if result:
        json_data = json.loads(result['data'])
        json_data.update(new_config)
        cursor.execute("UPDATE recommendations SET data = %s WHERE mid = 1", (json.dumps(json_data),))
        conn.commit()
        conn.close()
        return jsonify({"message": "Configuration updated successfully"}), 200
    else:
        return jsonify({"error": "No data found"}), 404
      
@app.route('/partialconf', methods=['GET'])
def get_partial_conf():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT data FROM recommendations WHERE mid = 1")
    result = cursor.fetchone()
    conn.close()
    if result:
        return jsonify(json.loads(result['data'])), 200
    else:
        return jsonify({"error": "No data found"}), 404
      

@app.route('/api/select', methods=['GET'])
def get_select_recommendations():
    data = {
  "results": [
    {
      "id": 1,
      "image": "https://www.selectfashion.co.uk/media/catalog/product/s/0/s059_2003_005_grey-2.jpg",
      "title": "Grey Belted Cargo Trousers",
      "sellPrice": "27.99",
      "currency":"£"
    },
    {
      "id": 2,
      "image": "https://www.selectfashion.co.uk/media/catalog/product/s/0/s059_2002_002_light-grey-_2_.jpg",
      "title": "LIGHT GREY HIGH WAISTED SKINNY JEAN",
      "sellPrice": "12.99",
      "currency":"£"
    },
    {
      "id": 3,
      "image": "https://www.selectfashion.co.uk/media/catalog/product/s/0/s059_2002_001_blue-acid.jpg",
      "title": "Blue Acid Carpenter Loose Fit Jeans",
      "sellPrice": "19.99",
      "currency":"£"
    },
    {
      "id": 4,
      "image": "https://www.selectfashion.co.uk/media/catalog/product/s/0/s059_1103_002_grey-1-.jpg",
      "title": "GREY PINSTRIPE WIDE LEG TROUSER",
      "sellPrice": "29.99",
      "currency":"£"
    },
    {
      "id": 5,
      "image": "https://www.selectfashion.co.uk/media/catalog/product/s/0/s059_1103_007_grey-3.jpg",
      "title": "GREY CONTRAST WAISTBAND TAILORED TROUSER",
      "sellPrice": "9.99",
      "currency":"£"
    },
    {
      "id": 6,
      "image": "https://www.selectfashion.co.uk/media/catalog/product/s/0/s059_1103_013_khaki-3.jpg",
      "title": "Khaki Linen Wide Leg Trousers",
      "sellPrice": "22.99",
      "currency":"£"
    },
    {
      "id": 7,
      "image": "https://www.selectfashion.co.uk/media/catalog/product/s/0/s058_2002_008_black-9.jpg",
      "title": "Black Ripped Mid Rise Jeans",
      "sellPrice": "14.99",
      "currency":"£"
    },
    {
      "id": 8,
      "image": "https://www.selectfashion.co.uk/media/catalog/product/s/0/s059_1103_013_black-6.jpg",
      "title": "Black Linen Wide Leg Trousers",
      "sellPrice": "22.99",
      "currency":"£"
    },
    {
      "id": 9,
      "image": "https://www.selectfashion.co.uk/media/catalog/product/s/0/s059_1103_016_black-7.jpg",
      "title": "Black Side Stripe Wide Leg Trousers",
      "sellPrice": "25.99",
      "url": "https://www.selectfashion.co.uk/black-side-stripe-wide-leg-trouser-s0591103016",
      "currency":"£"
    },
    {
      "id": 10,
      "image": "https://www.selectfashion.co.uk/media/catalog/product/s/0/s059_1103_015_khaki-2.jpg",
      "title": "Khaki Printed Wide Leg Cropped Trousers",
      "sellPrice": "19.99",
      "url": "https://www.selectfashion.co.uk/khaki-printed-wide-leg-cropped-trouser-s0591103015",
      "currency":"£"
    },
    {
      "id": 11,
      "image": "https://www.selectfashion.co.uk/media/catalog/product/s/0/s059_2002_003_bleachwsh-denim-11.jpg",
      "title": "Bleachwsh Denim Ripped Mid Rise Jeans",
      "sellPrice": "17.99",
      "url": "https://www.selectfashion.co.uk/bleachwsh-denim-ripped-mid-rise-jean-s0592002003",
      "currency":"£"
    },
    {
      "id": 12,
      "image": "https://www.selectfashion.co.uk/media/catalog/product/s/0/s058_2002_001_lightwash-9.jpg",
      "title": "Lightwash Straight Cuff Hem Jeans",
      "sellPrice": "12.99",
      "url": "https://www.selectfashion.co.uk/lightwash-straight-cuff-hem-jean-s0582002001",
      "currency":"£"
    },
    {
      "id": 13,
      "image": "https://www.selectfashion.co.uk/media/catalog/product/s/0/s058_2002_001_black-11.jpg",
      "title": "Black Straight Cuff Hem Jeans",
      "sellPrice": "12.99",
      "url": "https://www.selectfashion.co.uk/black-straight-cuff-hem-jean-s0582002001",
      "currency":"£"
    },
    {
      "id": 14,
      "image": "https://www.selectfashion.co.uk/media/catalog/product/s/0/s059_0502_019_grey-marl-3.jpg",
      "title": "Grey Marl Foldover Flares",
      "sellPrice": "14.99",
      "url": "https://www.selectfashion.co.uk/grey-marl-foldover-flares-s0590502019",
      "currency":"£"
    },
    {
      "id": 15,
      "image": "https://www.selectfashion.co.uk/media/catalog/product/s/0/s059_2003_002_stone-2.jpg",
      "title": "Stone Front Pocket Straight Leg Cargo Trousers",
      "sellPrice": "19.99",
      "url": "https://www.selectfashion.co.uk/stone-front-pocket-straight-leg-cargo-s0592003002",
      "currency":"£"
    },
    {
      "id": 16,
      "image": "https://www.selectfashion.co.uk/media/catalog/product/s/0/s059_2002_004_midwash-1.jpg",
      "title": "MIDWASH STRAIGHT LEG JEAN",
      "sellPrice": "17.99",
      "url": "https://www.selectfashion.co.uk/midwash-straight-leg-jean-s0592002004",
      "currency":"£"
    },
    {
      "id": 17,
      "image": "https://www.selectfashion.co.uk/media/catalog/product/m/i/miss-foxy-13th-april0283.jpg",
      "title": "DENIM BLUE Flared patchwork jeans ",
      "sellPrice": "31.99",
      "url": "https://www.selectfashion.co.uk/denim-blue-flared-patchwork-jeans-mfoxtrou0109",
      "currency":"£"
    },
    {
    "id": 18,
    "image": "https://www.selectfashion.co.uk/media/catalog/product/s/0/s058_2002_003_khaki-4.jpg",
    "title": "Khaki Contrast Stitch Cargo Jeans",
    "sellPrice": "14.99",
    "url": "https://www.selectfashion.co.uk/khaki-contrast-stitch-cargo-jean-s0582002003",
    "currency":"£"
    }
  ]}
    return jsonify(data)

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    url = "https://www.myntra.com/gateway/v2/product/26830734/related"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        products = data['related'][0]['products']
        formatted_products = []

        for product in products:
            formatted_product = {
                'brand': product['brand']['name'],
                'title': product['info'],
                'MRP': product['sellPrice']['mrp'],
                'discountedsellPrice': product['sellPrice']['discounted'],
                'discountLabel': product['sellPrice']['discount']['label'],
                'rating': product['rating'],
                'image': product['defaultImage']['secureSrc']
            }
            formatted_products.append(formatted_product)

        return jsonify(formatted_products)
    else:
        return jsonify({'error': f'Failed to fetch data. Status code: {response.status_code}'}), response.status_code


if __name__ == '__main__':
    app.run(debug=True)