from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "I'm comming to get you shmuli!"

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')
    # Add your scraping logic here
    return jsonify({"success": True, "message": f"Successfully scraped data from {url}", "data": {}})

if __name__ == '__main__':
    app.run()
