from flask import Flask, request, jsonify
from selenium import webdriver
import os

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), options=chrome_options)
    driver.get(url)
    page_content = driver.page_source
    driver.quit()

    return jsonify({'content': page_content})

if __name__ == '__main__':
    app.run(debug=True)
