import os
import requests
import json
from flask import (
    Flask,
    request,
    send_file,
    render_template,
    jsonify,
    Response,
    redirect,
    url_for,
)

from synthesys import synthesize
from text_processer import normalize_text, normalize_multiline_text

import webbrowser

DIR = "C:/YainTTS/models"

app = Flask(__name__)


@app.after_request
def allow_cors(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response


@app.route("/")
def index():
    return redirect(url_for("text_inference"))


@app.route("/tts-server/text-inference")
def text_inference():
    return render_template("text-inference.html")


@app.route("/tts-server/cc-overlay")
def open_captions_overlay():
    return render_template("cc-overlay.html")


@app.route("/tts-server/api/process-text", methods=["POST"])
def text():
    text = request.json.get("text", "")
    texts = normalize_multiline_text(text)

    return jsonify(texts)


@app.route("/tts-server/api/infer-glowtts")
def infer_glowtts():
    text = request.args.get("text", "")
    text = normalize_text(text).strip()

    if not text:
        return "text shouldn't be empty", 400

    try:
        wav = synthesize(text)
        return send_file(wav, mimetype="audio/wav", download_name="audio.wav")

    except Exception as e:
        return f"Cannot generate audio: {str(e)}", 500

@app.route("/api/models")
def get_models():
    models_res = []
    models = next(os.walk(DIR))[1]
    for i in range(len(models)):
        with open(os.path.join(DIR,models[i],"conf.json"), "r", encoding="utf8") as f:
            out = json.loads(f.read())
            models_res.append(out.get("name"))
    # if env set
    if "TTS_MODEL_FILE" in os.environ:
        with open(os.path.join(DIR,os.environ.get("TTS_MODEL_FILE").split('/')[-3],"conf.json"), "r", encoding="utf8") as f:
            out = json.loads(f.read())
            current = (out.get("name"))
    else:
        current = models_res[0]
    return json.dumps({"models":models_res,"selected":current}), 200

#post
@app.route("/api/models", methods=["POST"])
def post_models():
    name = request.json.get("model", "")
    if not name:
        return "name shouldn't be empty", 400
    models = next(os.walk(DIR))[1]
    for i in range(len(models)):
        with open(os.path.join(DIR,models[i],"conf.json"), "r", encoding="utf8") as f:
            out = json.loads(f.read())
            if out.get("name") == name:
                os.environ['TTS_MODEL_FILE']="/".join([DIR,models[i],'glowtts-v2/best_model.pth.tar'])
                os.environ['TTS_MODEL_CONFIG']="/".join([DIR,models[i],'glowtts-v2/config.json'])
                os.environ['VOCODER_MODEL_FILE']="/".join([DIR,models[i],'hifigan-v2/best_model.pth.tar'])
                os.environ['VOCODER_MODEL_CONFIG']="/".join([DIR,models[i],'hifigan-v2/config.json'])
                return "success", 200
    return "model not found", 404
    
@app.route("/favicon.ico")
def favicon():
    return "I don't have favicon :p", 404


@app.route("/<path:path>")
def twip_proxy(path):
    new_url = request.url.replace(request.host, "twip.kr")
    resp = requests.request(
        method=request.method,
        url=new_url,
        headers={key: value for (key, value) in request.headers if key != "Host"},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
    )
    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]
    headers = [
        (name, value)
        for (name, value) in resp.raw.headers.items()
        if name.lower() not in excluded_headers
    ]
    content = resp.content
    if new_url.startswith("http://twip.kr/assets/js/alertbox/lib-"):
        content = (
            resp.text
            + f"""
        const original_function = Howl.prototype.init;
        Howl.prototype.init = function (o) {{
            if (o.src.startsWith('https://www.google.com/speech-api/v1/synthesize?text=')) {{
                o.src = o.src.replace(
                    'https://www.google.com/speech-api/v1/synthesize?text=',
                    '/tts-server/api/infer-glowtts?text='
                );
                o.html5 = false;
                o.volume = o.volume * 2;
            }}
            return original_function.call(this, o);
        }}
        """
        )
    response = Response(content, resp.status_code, headers)
    return response


if __name__ == "__main__":
    webbrowser.open("http://localhost:5000/")
    app.run(host="0.0.0.0", debug=os.environ.get("TTS_DEBUG", "0") == "1")