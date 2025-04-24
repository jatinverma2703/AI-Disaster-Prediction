from flask import Flask, render_template, request, redirect, send_file, url_for, jsonify
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess

app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/detect", methods=['POST'])
def detect():
    if request.method != "POST":
        return "Invalid request method", 400

    video = request.files.get('video')
    if not video:
        return "No video file provided", 400

    filename = secure_filename(video.filename)
    video_path = os.path.join("static", filename)
    video.save(video_path)

    output_filename = filename
    output_path = os.path.join("static", output_filename)

    subprocess.run(['python', 'detect.py', '--source', video_path])

    if os.path.exists(output_path):
        return send_file(output_path, mimetype='video/mp4')
    else:
        return "Processing failed", 500


@app.route('/return-files', methods=['GET'])
def return_file():
    files = os.listdir(uploads_dir)
    return jsonify({'files': files})


if __name__ == "__main__":
    app.run(debug=False)
