from flask import Flask, send_from_directory, abort
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

PHOTOS_DIR = Path("/home/roruck/iotcam/motion_pics")

@app.route("/")
def index():
    photos = []

    if PHOTOS_DIR.exists():
        for f in PHOTOS_DIR.iterdir():
            if f.is_file() and f.suffix.lower() == ".jpg":
                stat = f.stat()
                photos.append({
                    "name": f.name,
                    "time": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    "mtime": stat.st_mtime
                })

    photos.sort(key=lambda x: x["mtime"], reverse=True)

    html = """
    <!DOCTYPE html>
    <html lang="lt">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="10">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IoT kameros galerija</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background: #f4f4f4;
                color: #222;
            }
            .box {
                background: white;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            img {
                max-width: 100%;
                height: auto;
                border-radius: 8px;
            }
            a {
                color: #0056b3;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            ul {
                padding-left: 20px;
            }
            li {
                margin-bottom: 8px;
            }
            .small {
                color: #666;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <h1>IoT kameros galerija</h1>
        <p class="small">Puslapis atsinaujina kas 10 sekundžių</p>
    """

    if photos:
        latest = photos[0]
        html += f"""
        <div class="box">
            <h2>Paskutinė nuotrauka</h2>
            <a href="/photo/{latest['name']}" target="_blank">
                <img src="/photo/{latest['name']}" alt="Paskutinė nuotrauka">
            </a>
            <p><strong>{latest['name']}</strong></p>
            <p class="small">{latest['time']}</p>
        </div>
        """

        html += """
        <div class="box">
            <h2>Paskutinės nuotraukos</h2>
            <ul>
        """

        for photo in photos[:10]:
            html += f'<li><a href="/photo/{photo["name"]}" target="_blank">{photo["name"]}</a> — {photo["time"]}</li>'

        html += """
            </ul>
        </div>
        """
    else:
        html += """
        <div class="box">
            <h2>Paskutinė nuotrauka</h2>
            <p>Nuotraukų dar nėra.</p>
        </div>
        """

    html += """
    </body>
    </html>
    """

    return html

@app.route("/photo/<filename>")
def photo(filename):
    file_path = PHOTOS_DIR / filename
    if not file_path.exists():
        abort(404)
    return send_from_directory(PHOTOS_DIR, filename)

@app.route("/health")
def health():
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
