from flask import Flask
import os

app = Flask(__name__)

if __name__ == "__main__":
    # Fallback to 8000 if PORT environment variable is missing
    port = int(os.environ.get("PORT", 8000)) # Changed default port to 8000
    app.run(host="0.0.0.0", port=port)
