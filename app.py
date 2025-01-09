from flask import Flask, Response
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/view/<id>')
def mirror(id):
    url = f'https://cache.animetosho.org/nyaasi/view/{id}'
    
    try:
        print(f"Fetching URL: {url}")  # Log the URL being fetched
        response = requests.get(url)

        print(f"Response Code: {response.status_code}")  # Log the response code

        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 1. Find the CSS link tag and update its href attribute
            css_link = soup.find('link', rel='stylesheet')
            if css_link:
                css_link['href'] = 'https://cache.animetosho.org/style.css?t=1719980696049.208'
            
            # 2. Find the GitHub link and replace it with the Telegram link and icon
            github_link = soup.find('a', id='header_right')
            if github_link:
                github_link['href'] = 'https://t.me/nyaatorrents'  # Change to Telegram URL
                telegram_icon = soup.new_tag('img', src='https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/512px-Telegram_logo.svg.png?20220101141644', alt='Telegram')
                telegram_icon['id'] = 'tg_icon'  # Optional: Add an ID for the icon
                github_link.clear()  # Clear the existing content (GitHub icon)
                github_link.append(telegram_icon)  # Append the Telegram icon
                
            # Convert the modified HTML back to a string
            modified_html = str(soup)
            
            return Response(modified_html, content_type='text/html')
        else:
            print(f"Error fetching the content: {response.status_code}")  # Log error details
            return f"Error fetching the content: {response.status_code}", response.status_code
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {str(e)}")  # Log exceptions
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
