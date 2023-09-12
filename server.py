from flask import Flask, render_template, request, jsonify, send_file
from gpt import get_bot_response, get_ocr_result
import base64
import os
# Define constants
IMAGE_FOLDER = 'static/img'

app = Flask(__name__, template_folder='views')
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

# Define symptom checker API
@app.route('/api/symptom-check', methods=['POST'])
def check():
    result = ''
    # Get form data
    symptom = request.form.get('symptom')
    age = request.form.get('age')
    gender = request.form.get('gender')
    report = request.files.get('report')

    # Process image
    if report:
        file_data = report.read()
        file_base64 = base64.b64encode(file_data).decode('utf-8')
        ocr_result = get_ocr_result(file_base64)
        prompt = "Symptom: " + str(symptom) + ", " + "Age: " + str(age) + ", " + "Gender: " + str(gender) + ", " + "Check report: " + str(ocr_result)
    else:
        prompt = "Symptom: " + str(symptom) + ", " + "Age: " + str(age) + ", " + "Gender: " + str(gender)
    result = get_bot_response(prompt)
    return result

# Image file route function
@app.route('/<image_name>.png')
def get_image(image_name):
    return send_file(os.path.join(app.config['IMAGE_FOLDER'], f'{image_name}.png'), mimetype='image/png')


# Homepage route function
@app.route('/')
@app.route('/index.html')
@app.route('/result.html')
def index():
    return render_template(request.path[1:] or 'index.html')

if __name__ == '__main__':
    # Optimize the way the application runs
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
