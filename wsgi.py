from waitress import serve
from __init__ import app

print("Hello 👋 Server is starting...")
serve(app, host="0.0.0.0", port=8080)