# Assignment:
# 1. Allow user to upload an image file consisting of data (example invoice)
# 2. Write logic to extract the data from the image
# 3. Allow user to schedule the time he/she can extract the data from the image
# 4. Upload it on vercel app or pythonanywhere or on streamlit or on similar website and share the url
import os  # For File Manipulations like get paths, rename
from datetime import datetime

# import time
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
# from werkzeug import secure_filename

from flask import Flask, render_template, request, flash

UPLOAD_FOLDER = 'static/upload/'
app = Flask(__name__)
app.secret_key = "secret key"  # for encrypting the session

folder = os.getcwd() + '/static/upload/'


# now = datetime.now()


@app.route("/", methods=['GET', 'POST'])
def dashboard():
    text = ""
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template('index.html', text='No File Part')

        f = request.files['file']
        if f.filename == '':
            flash('No file selected for uploading')
            return render_template('index.html', text='No file selected for uploading')

        if f and allowed_file(f.filename):
            f = request.files['file']
            # file.save(os.path.join( / path / to / save /, filename))
            h = int(request.form.get('hour'))
            m = int(request.form.get('min'))
            hour = f'{h:02d}'
            min = f'{m:02d}'
            print(hour, min)
            # ap=request.form.get('ap')

            # current_time = now.strftime("%H:%M")
            print(hour)
            usert = hour + ':' + min + ':' + '00'
            if usert == '00:00:00':
                text = imgtotext(f)
                return render_template('index.html', text=text)
            else:
                # print('failed')
                text = call(usert, f)
                return render_template('index.html', text=text)

        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            text = 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'
            return render_template('index.html', text=text)

    # print(text,type(text))

    return render_template('index.html',text=text)


def call(usert, f):
    current = str(datetime.now().strftime("%H:%M:%S"))
    while (current != usert):
        # print(current)
        print(usert)
        current = str(datetime.now().strftime("%H:%M:%S"))
    text = imgtotext(f)
    # deletefile()
    return text


ALLOWED_EXTENSIONS = set(['PNG', 'JPEG', 'PPM', 'GIF', 'TIFF', 'BMP', 'JPG','png','jpeg','jpg','gif','tiff','bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def imgtotext(f):
    f.save(os.path.join(folder, f.filename))
    text = pytesseract.image_to_string(Image.open(folder + f.filename))
    deletefile()
    return text


def deletefile():
    for file in os.listdir(folder):
        os.remove(os.path.join(folder, file))


# def ocr_core(filename):
#     """
#     This function will handle the core OCR processing of images.
#     """
#     text = pytesseract.image_to_string(Image.open(filename))
#     return text
#
#
# print(ocr_core('images/ocr_example_1.png'))
if __name__ == "__main__":
    app.run()
