from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from image_processing import edge_detection
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['PROCESSED_FOLDER'] = 'processed/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File successfully uploaded'
    else:
        return 'File type not allowed'

@app.route('/images')
def list_images():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    selected_image = request.args.get('filename')
    return render_template('list_images.html', images=images, selected_image=selected_image)

@app.route('/uploads/<filename>')
def display_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/process/<filename>', methods=['GET', 'POST'])
def process_image(filename):
    if request.method == 'POST':
        threshold1 = int(request.form.get('threshold1', 100))
        threshold2 = int(request.form.get('threshold2', 200))
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        processed_image_path = edge_detection(image_path, app.config['PROCESSED_FOLDER'], threshold1, threshold2)
        return render_template('process_image.html', filename=filename, processed_image=os.path.basename(processed_image_path))
    else:
        return render_template('process_image.html', filename=filename)



@app.route('/processed/<filename>')
def display_processed_image(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)