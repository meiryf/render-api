from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "I'm coming to get you, Shmuli!"

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"success": False, "message": "Invalid input: 'url' field is required"}), 400
    url = data.get('url')
    # Add your scraping logic here
    return jsonify({"success": True, "message": f"Successfully scraped data from {url}", "data": {}})

if __name__ == '__main__':
    app.run()
