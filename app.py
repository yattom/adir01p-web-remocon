"""スマホから操作する Web リモコン。"""
from flask import Flask, jsonify, render_template

import ir

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.get("/")
def index():
    buttons = {
        b["id"]: {**b, "learned": (ir.CODES / f"{b['id']}.txt").exists()}
        for b in ir.load_buttons()
    }
    return render_template("index.html", b=buttons)


@app.post("/send/<button_id>")
def send(button_id: str):
    try:
        ir.send(button_id)
    except ir.IRError as e:
        app.logger.warning("send %s failed: %s", button_id, e)
        return jsonify(ok=False, error=str(e)), 500
    return jsonify(ok=True)


@app.get("/manifest.webmanifest")
def manifest():
    return app.response_class(
        '{"name": "リモコン", "short_name": "リモコン", "start_url": "/", '
        '"display": "standalone", "background_color": "#a07850", "theme_color": "#a07850", '
        '"icons": [{"src": "/static/icon-192.png", "sizes": "192x192", "type": "image/png"}, '
        '{"src": "/static/icon-512.png", "sizes": "512x512", "type": "image/png"}]}',
        mimetype="application/manifest+json",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, threaded=True)
