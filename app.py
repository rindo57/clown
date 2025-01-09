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
            
            # Find the CSS link tag and update its href attribute
            css_link = soup.find('link', rel='stylesheet')
            if css_link:
                css_link['href'] = 'https://cache.animetosho.org/style.css?t=1719980696049.208'
            
            # Replace GitHub icon with Telegram icon in the header
            telegram_icon_svg = '''
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/512px-Telegram_logo.svg.png?20220101141644" alt="Telegram Icon" width="24" height="24">
            '''
            telegram_link = f'<a id="header_right" href="https://t.me/nyaatorrents">{telegram_icon_svg}</a>'
            
            # Modify the header to replace GitHub with Telegram
            header = soup.find('header')
            if header:
                # Replace the GitHub icon section with the Telegram link
                telegram_anchor = header.find('a', {'id': 'header_right'})
                if telegram_anchor:
                    telegram_anchor.replace_with(telegram_link)  # Ensure it's replaced with the full Telegram link
            
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
