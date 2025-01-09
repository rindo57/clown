from flask import Flask, Response
import requests

app = Flask(__name__)

@app.route('/view/<id>')
def mirror(id):
    url = f'https://cache.animetosho.org/nyaasi/view/{id}'
    
    try:
        print(f"Fetching URL: {url}")  # Log the URL being fetched
        response = requests.get(url)

        print(f"Response Code: {response.status_code}")  # Log the response code

        if response.status_code == 200:
            return Response(response.content, content_type=response.headers['Content-Type'])
        else:
            print(f"Error fetching the content: {response.status_code}")  # Log error details
            return f"Error fetching the content: {response.status_code}", response.status_code
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {str(e)}")  # Log exceptions
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', host=80, debug=True)
