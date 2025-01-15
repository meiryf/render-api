from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "I'm coming to get you, Shmuli!"

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.get_json(force=True)
        if not data or 'url' not in data:
            app.logger.error("Invalid input: 'url' field is required")
            return jsonify({"success": False, "message": "Invalid input: 'url' field is required"}), 400
        url = data.get('url')
        # Add your scraping logic here
        app.logger.info(f"Successfully scraped data from {url}")
        return jsonify({"success": True, "message": f"Successfully scraped data from {url}", "data": {}})
    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({"success": False, "message": "An error occurred"}), 500

if __name__ == '__main__':
    app.run()
