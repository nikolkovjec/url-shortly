from flask import Flask, jsonify, redirect, request
import hashlib
import base64

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'  # replace with your server name

# In-memory storage for short-to-long URL mappings
url_map = {}

# Generate a unique ID for a given URL
def generate_id(url):
    # Hash the URL to generate a unique ID
    md5 = hashlib.md5()
    md5.update(url.encode('utf-8'))
    id_bytes = md5.digest()

    # Use base64 encoding to convert bytes to a string
    # This makes the ID shorter and easier to read
    id_str = base64.urlsafe_b64encode(id_bytes).decode('utf-8')

    # Remove any padding characters from the end of the string
    return id_str.rstrip('=')

# Endpoint to generate a shortened URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json['url']
    if long_url in url_map.values():
        # URL already exists, return existing shortened URL
        for short_url, stored_url in url_map.items():
            if stored_url == long_url:
                return jsonify({'short_url': short_url})

    # Generate a new shortened URL
    while True:
        short_url = generate_id(long_url)
        if short_url not in url_map:
            url_map[short_url] = long_url
            return jsonify({'short_url': short_url})

# Endpoint to expand a shortened URL
@app.route('/<short_url>')
def expand_url(short_url):
    if short_url in url_map:
        long_url = url_map[short_url]
        return redirect(long_url, code=301)
    else:
        return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run()