# Import necessary modules
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Initialize the Flask application
app = Flask(__name__)

# Existing routes...
# If you have other routes, they will be defined here

# Define the new route for scraping
@app.route('/scrape', methods=['POST'])
def scrape():
    # Get JSON data from the request
    data = request.get_json()
    
    # Extract the URL from the request data
    url = data.get('url')
    
    # Check if URL is provided
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Set up Chrome options for headless mode (run without a visible browser window)
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Initialize ChromeDriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open the URL in the browser
        driver.get(url)

        # Find the first element with the class 'time'
        element = driver.find_element(By.CLASS_NAME, 'time')
        
        # Get the innerHTML of the element
        content = element.get_attribute('innerHTML')
        
        # Return the content as a JSON response
        return jsonify({'content': content})
    except Exception as e:
        # Handle any exceptions that occur and return an error response
        return jsonify({'error': str(e)}), 500
    finally:
        # Close the browser
        driver.quit()

# Main entry point of the application
if __name__ == '__main__':
    app.run(debug=True)
