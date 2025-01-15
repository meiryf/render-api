from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        app.logger.error('URL is required')
        return jsonify({'error': 'URL is required'}), 400

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize ChromeDriver
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        app.logger.error(f'Error initializing ChromeDriver: {e}')
        return jsonify({'error': 'Failed to initialize ChromeDriver'}), 500

    try:
        # Open the URL
        driver.get(url)

        # Find the first element with the class 'time'
        element = driver.find_element(By.CLASS_NAME, 'time')
        content = element.get_attribute('innerHTML')
        
        app.logger.info(f'Successfully scraped content: {content}')
        return jsonify({'content': content})
    except Exception as e:
        app.logger.error(f'Error occurred during scraping: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
