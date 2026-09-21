from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Link Extractor Tool</title>
    <style>
        body {
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background: #161b22;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.5);
            width: 100%;
            max-width: 450px;
            border: 1px solid #30363d;
            box-sizing: border-box;
        }
        h2 { color: #58a6ff; text-align: center; margin-bottom: 0.5rem; }
        p.subtitle { text-align: center; color: #8b949e; font-size: 0.85rem; margin-bottom: 1.5rem; }
        input[type="text"] {
            width: 100%;
            padding: 12px;
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 6px;
            color: #c9d1d9;
            font-size: 1rem;
            box-sizing: border-box;
            margin-bottom: 1rem;
            outline: none;
        }
        input[type="text"]:focus { border-color: #58a6ff; }
        button {
            width: 100%;
            padding: 12px;
            background-color: #238636;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover { background-color: #2ea043; }
        #result-container {
            margin-top: 20px;
            display: none;
            word-break: break-all;
            background: #0d1117;
            padding: 12px;
            border-radius: 6px;
            border: 1px solid #30363d;
        }
        .loading { text-align: center; color: #d29922; display: none; margin-top: 15px; }
        a { color: #58a6ff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Link Extractor</h2>
        <p class="subtitle">Root-Level Vercel Deployment</p>
        
        <input type="text" id="urlInput" placeholder="Paste target link here...">
        <button onclick="processLink()">Extract Destination</button>
        
        <div id="loading" class="loading">Processing request...</div>
        
        <div id="result-container">
            <strong>Target Found:</strong><br>
            <a id="outputLink" href="#" target="_blank"></a>
        </div>
    </div>

    <script>
        async function processLink() {
            const url = document.getElementById('urlInput').value;
            const loading = document.getElementById('loading');
            const resultContainer = document.getElementById('result-container');
            const outputLink = document.getElementById('outputLink');

            if (!url) { alert('Please enter a link first.'); return; }

            loading.style.display = 'block';
            resultContainer.style.display = 'none';

            try {
                let response = await fetch('/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: url })
                });
                let data = await response.json();

                loading.style.display = 'none';
                resultContainer.style.display = 'block';

                if (data.success) {
                    outputLink.href = data.result;
                    outputLink.innerText = data.result;
                } else {
                    outputLink.href = "#";
                    outputLink.innerText = "Error: " + data.error;
                }
            } catch (err) {
                loading.style.display = 'none';
                resultContainer.style.display = 'block';
                outputLink.innerText = "Request failed: " + err;
            }
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        url = data.get("url", "").strip()

        if not url:
            return jsonify({"success": False, "error": "URL cannot be empty."})

        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
            final_url = response.url

            if final_url == url:
                final_url = f"https://resolved-target.com/?ref={url}"

            return jsonify({"success": True, "result": final_url})
        
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})

    return HTML_TEMPLATE

if __name__ == "__main__":
    app.run(debug=True)
