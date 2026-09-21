import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/bypass", methods=["POST"])
def bypass():
    data = request.get_json()
    url = data.get("url", "").strip()
    
    if not url:
        return jsonify({"success": False, "error": "URL cannot be empty."})

    try:
        # Core resolver logic or integration call
        # Note: Direct requests logic placeholder. Shortener gates usually require 
        # handling unique API/token tokens depending on active backend structures.
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        # Simulating request check (Replace with your parsing logic or upstream solver API)
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        final_url = response.url

        if final_url == url:
            # If no automatic redirect happened, mock or parse out parameters if applicable
            final_url = f"https://resolved-target.com/?ref={url}"

        return jsonify({"success": True, "result": final_url})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
