from flask import Flask, request, redirect, url_for, render_template
from google.cloud import storage
from flask_cors import CORS
import os

app = Flask(__name__)
# Setting max file size
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  

# Configure the Google Cloud Storage client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../vertexproj/google-cloud.json"
client = storage.Client()
bucket_name = 'dev-videos'
bucket = client.bucket(bucket_name)

@app.route('/')
def upload_form():
    return render_template("upload.html")

@app.route('/', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return redirect(request.url)
    file = request.files['video']
    if file.filename == '':
        return redirect(request.url)
    if file:
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
        return f'File {file.filename} uploaded to {bucket_name}.'

if __name__ == "__main__":
    app.run(debug=True)