from flask import Flask, request, jsonify
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

SCRAPINGBEE_API_KEY = 'your_scrapingbee_api_key'

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        app.logger.error('URL is required')
        return jsonify({'error': 'URL is required'}), 400

    try:
        response = requests.get(
            'https://app.scrapingbee.com/api/v1/',
            params={
                'api_key': SCRAPINGBEE_API_KEY,
                'url': url,
                'render_js': 'true'
            }
        )
        response.raise_for_status()
        content = response.text
        
        app.logger.info(f'Successfully scraped content: {content[:500]}')  # Log the first 500 characters
        return jsonify({'content': content})
    except Exception as e:
        app.logger.error(f'Error occurred during scraping: {e}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
