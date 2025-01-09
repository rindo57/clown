from flask import Flask, Response, send_file
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route('/view/<id>')
def mirror(id):
    url = f'https://cache.animetosho.org/nyaasi/view/?id={id}'
    
    try:
        print(f"Fetching URL: {url}")  # Log the URL being fetched
        response = requests.get(url)

        print(f"Response Code: {response.status_code}")  # Log the response code

        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find and update the CSS link tag
            css_link = soup.find('link', rel='stylesheet')
            if css_link:
                css_link['href'] = '/static/pizza.css'
            
            # Find and remove the "Anime Tosho" link
            header_left = soup.find('span', id='header_left')
            if header_left:
                anime_tosho_link = header_left.find('a', href='https://animetosho.org/')
                if anime_tosho_link:
                    anime_tosho_link.decompose()  # Removes the "Anime Tosho" link completely
                
                # Replace the "Nyaa.si Cache" link with the new URL
                nyaa_si_cache_link = header_left.find('a', href='/nyaasi/')
                if nyaa_si_cache_link:
                    nyaa_si_cache_link['href'] = 'https://nyaa.si'  # Update href to "https://nyaa.si"

            # Modify the "Download Torrent" link by changing only the domain
            torrent_link = soup.find('a', href=True, string="📄 Download Torrent")
            if torrent_link:
                original_torrent_url = torrent_link['href']
                if "https://storage.animetosho.org/" in original_torrent_url:
                    torrent_link['href'] = original_torrent_url.replace("https://storage.animetosho.org/", "https://cache.ddlserverv1.me.in/")



            # Find the GitHub link and replace it with the Telegram link and icon
            github_link = soup.find('a', id='header_right')
            if github_link:
                github_link['href'] = 'https://t.me/nyaatorrents'  # Change to Telegram URL
                telegram_icon = soup.new_tag('img', 
                                             src='https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/512px-Telegram_logo.svg.png?20220101141644', 
                                             alt='Telegram')
                telegram_icon['id'] = 'tg_icon'  # Optional: Add an ID for the icon
                telegram_icon['width'] = '32'  # Set the width to 32px
                telegram_icon['height'] = '32'  # Set the height to 32px
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

# Direct Streaming

@app.route('/nyaasi_archive/<id>/<text>')
def download_torrent(id, text):
    # Construct the real torrent URL from Animetosho
    torrent_url = f"http://storage.animetosho.org/nyaasi_archive/{id}/{text}"
    
    # Fetch the torrent file from Animetosho and stream it directly to the user
    try:
        response = requests.get(torrent_url, stream=True)
        
        if response.status_code == 200:
            # Stream the file directly to the user
            return Response(response.iter_content(1024), 
                            content_type="application/x-bittorrent", 
                            headers={"Content-Disposition": f"attachment; filename={id}.torrent"})
        else:
            return f"Error fetching the torrent file: {response.status_code}", response.status_code
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {str(e)}", 500

"""
@app.route('/nyaasi_archive/<id>/<text>')
def download_torrent(id, text):
    # Construct the real torrent URL from animetosho
    torrent_url = f"http://storage.animetosho.org/nyaasi_archive/{id}/{text}"
    # Fetch the torrent file from animetosho
    response = requests.get(torrent_url, stream=True)

    if response.status_code == 200:
        # Create a temporary file to stream the content to the user
        temp_file = os.path.join("/tmp", f"{id}.torrent")
        
        # Write the content to the temporary file
        with open(temp_file, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        
        # Send the file as a response
        return send_file(temp_file, as_attachment=True, download_name=f"{id}.torrent", mimetype="application/x-bittorrent")
    
    else:
        return f"Error fetching the torrent file: {response.status_code}", response.status_code
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
