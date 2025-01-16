from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Replace with your actual ScrapingBee API key
SCRAPINGBEE_API_KEY = 'HPZIQ2M50SWF3WM30TVCUBW0LQNTJGUQUDPTJIFL62I7D45OMQ5I90ZAM74IGR0MP7S1KAD1I6XPYKQT'

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
        
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the first element with the class 'time'
        element = soup.find(class_='time')
        
        if element:
            inner_html = element.decode_contents()
            app.logger.info(f'Successfully scraped content: {inner_html}')
            return jsonify({'content': inner_html})
        else:
            app.logger.error('Element with class "time" not found')
            return jsonify({'error': 'Element with class "time" not found'}), 404
        
    except Exception as e:
        app.logger.error(f'Error occurred during scraping: {e}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
