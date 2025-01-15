from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

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
    result = scrape_content(url)
    if result['success']:
        return jsonify({"success": True, "message": f"Successfully scraped data from {url}", "data": result['content']})
    else:
        return jsonify({"success": False, "message": result['error']}), 500

def scrape_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content = '\n'.join([p.get_text() for p in paragraphs])
        return {"success": True, "content": content}
    except requests.RequestException as e:
        return {"success": False, "error": str(e)}

if __name__ == '__main__':
    app.run()
