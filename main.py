#Sebastian Rojas, 1/20/2025, https://sebasrojas-uploader-740894791792.us-central1.run.app/
#I decided to use your skeleton code as you said, but i decided to switch from the inline html to external since its easier to read and write on.
#it took a lot of research to figure out how to show the image submitted into the page
import os
from flask import Flask, redirect, request, render_template, url_for
from google.cloud import storage

app = Flask(__name__)

BUCKET_NAME = os.environ.get("BUCKET_NAME", "sebasrojas")

@app.route('/')
def index():
    #lists images
    files = list_files()
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    #gets the file 
    file = request.files.get('form_file')
    if file and file.filename:
        upload_file_to_gcs(file, file.filename)
    return redirect(url_for('index'))

@app.route('/files')
def list_files_endpoint():
    #returns list of images
    return {"files": list_files()}

def list_files():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blobs = bucket.list_blobs()

    valid_extensions = ('.jpg', '.jpeg')
    file_urls = []
    for blob in blobs:
        if blob.name.lower().endswith(valid_extensions):
            #makes the public url for the image submitted directly (This took a while)
            url = f"https://storage.googleapis.com/{BUCKET_NAME}/{blob.name}"
            file_urls.append(url)
    return file_urls


def upload_file_to_gcs(file_obj, filename):
    #uploads obj to gcs
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_file(file_obj, content_type=file_obj.content_type)
    
    return blob.public_url

if __name__ == '__main__':
    app.run(debug=True)
