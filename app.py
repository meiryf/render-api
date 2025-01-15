from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_binary  # Adds chromedriver binary to path

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open the URL
        driver.get(url)

        # Find the first element with the class 'time'
        element = driver.find_element(By.CLASS_NAME, 'time')
        content = element.get_attribute('innerHTML')
        
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)

