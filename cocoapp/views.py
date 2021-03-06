import os
import glob
from flask import Flask
from flask import jsonify
from flask import request, render_template

from cocoapp import app
from model.util import *
from cocoapp.cocomodel import *

valid_mimetypes = ['image/jpeg', 'image/png']


# def get_predictions(img_name):
#     #TODO
#     return {
#         "bboxes":
#         [
#             {"x1": 10, "x2": 50, "y1": 10, "y2": 50}
#         ],
#     }


@app.route('/')
def index():
    # app.logger.warning('sample message')
    # # Sort files by upload date
    # recent_files = sorted(
    #     glob.glob("%s/*" % app.config['SAMPLE_FOLDER']),
    #     key=os.path.getctime, reverse=True
    # )
    samples = glob.glob("%s/*" % app.config['SAMPLE_FOLDER'])
    # Pick the most recent two or less for the index view
    #slice_index = 2 if len(sample_files) > 1 else len(sample_files)
    #recents = sample_files[:slice_index]
    # app.logger.warning(samples[0][8:])
    return render_template('index.html', samples=samples)

    # return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'no file'}), 400
        # Image info
        img_file = request.files.get('file')
        img_name = img_file.filename
        mimetype = img_file.content_type
        # Return an error if not a valid mimetype
        if mimetype not in valid_mimetypes:
            return jsonify({'error': 'bad-type'})
        # Write image to static directory
        img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], img_name))

        img = open_image(os.path.join(app.config['UPLOAD_FOLDER'], img_name))
        # Run Prediction on the model
        results = get_predictions(img, True)

        # Delete image when done with analysis
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], img_name))

        return jsonify(results)
