from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time

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

    # Initialize ChromeDriver using webdriver_manager
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        chrome_service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    except Exception as e:
        app.logger.error(f'Error initializing ChromeDriver: {e}')
        return jsonify({'error': 'Failed to initialize ChromeDriver'}), 500

    try:
        # Open the URL
        driver.get(url)

        # Wait for Cloudflare verification to complete
        wait = WebDriverWait(driver, 60)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'time')))

        # Additional wait to ensure page loads completely
        time.sleep(20)  # Adjust the sleep time if needed

        # Log the HTML content of the page
        app.logger.info(f"Page HTML: {driver.page_source}")

        # Use explicit wait to wait for the element to be present
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'time')))

        # Get the innerHTML of the element
        content = element.get_attribute('innerHTML')
        
        app.logger.info(f'Successfully scraped content: {content}')
        return jsonify({'content': content})
    except Exception as e:
        app.logger.error(f'Error occurred during scraping: {e}')
        app.logger.error(f'HTML content: {driver.page_source}')  # Log the HTML content for troubleshooting
        return jsonify({'error': str(e)}), 500
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
