from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

        # Log the HTML content of the page
        app.logger.info(f"Page HTML: {driver.page_source}")

        # Use explicit wait to wait for the element to be present
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'time')))

        # Get the innerHTML of the element
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
