from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a random secret key in production

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Function to check file size (5 MB limit)
def is_file_size_valid(file):
    return file.content_length <= 5 * 1024 * 1024  # 5 MB


@app.route('/')
def home():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('home'))

    file = request.files['file']

    # If the user does not select a file, the browser also submits an empty part without a filename
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('home'))

    file_type = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'unknown'

    # Validate file
    if not allowed_file(file.filename):
        flash('File type not allowed')
        print(f"Potential file upload vulnerability detected: {file.filename} (type: {file_type})")
        return redirect(url_for('home'))

    if not is_file_size_valid(file):
        flash('File is too large, max size is 5 MB')
        return redirect(url_for('home'))

    # Save the file
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    flash(f'File uploaded successfully! File type: {file_type}')  # Show file type in the message
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
