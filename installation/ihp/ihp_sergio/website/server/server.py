import os

from flask import Flask, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PORT = 443
HOST = "127.0.0.1"
DEBUG = True

# Use SSH. Set a context with crt and key files and path it to app.run()
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          os.path.pardir))
crt_path = os.path.join(parent_dir, 'ssl', 'nginx.crt')
key_path = os.path.join(parent_dir, 'ssl', 'nginx.key')
context = (crt_path, key_path)

if not os.path.exists(crt_path) or not os.path.exists(crt_path):
    raise ValueError("Missing files for SSL context %s and/or %s."
                     % (crt_path, key_path))


@app.route('/', methods=['GET'])
def main():
    return redirect(url_for('static', filename='index.html'))


if __name__ == "__main__":
    app.run(HOST, PORT, DEBUG, ssl_context=context)
