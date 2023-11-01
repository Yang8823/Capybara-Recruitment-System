from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textract import process
from itertools import chain
import string
import re
import os
from joblib import load
import pickle
import en_core_web_sm
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
nlp = en_core_web_sm.load()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///response_data.db'
db = SQLAlchemy(app)
# Define your model and other Flask routes

CORS(app, resources={r"/process": {"origins": "http://localhost:8000"}})

# Define a model for your data
class ResponseData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.String(255))
    score = db.Column(db.Float)
    profile = db.Column(db.String(255))
    user_id = db.Column(db.String(255))
    tags = db.Column(db.String(255))
    job_description = db.Column(db.Text)

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()
    print("Database tables created successfully")
    
results_list = []

######################################

###### NLP MODEL SECTION #############


def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)
    resumeText = re.sub('RT|cc', ' ', resumeText)
    resumeText = re.sub('#\S+', '', resumeText)
    resumeText = re.sub('@\S+', '  ', resumeText)
    resumeText = re.sub('[%s]' % re.escape(
        """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)
    resumeText = re.sub(r'[^\x00-\x7f]', r' ', resumeText)
    resumeText = re.sub('\s+', ' ', resumeText)
    return resumeText


def Preprocessfile(filename):
    text = filename
    if ".pdf" in filename:
        try:
            text = extract_text_from_pdf(filename)
        except UnicodeDecodeError:
            print('File', filename, 'cannot be extracted! - skipped')
        text = text.replace("\\n", " ")
    else:
        text = text.replace("\\n", " ")
    x = []
    tokens = word_tokenize(text)
    tok = [w.lower() for w in tokens]
    table = str.maketrans('', '', string.punctuation)
    strpp = [w.translate(table) for w in tok]
    words = [word for word in strpp if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    x.append(words)
    res = " ".join(chain.from_iterable(x))
    return res

def extract_text_from_pdf(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as pdf_file:
        pdf = PyPDF4.PdfFileReader(pdf_file)
        for page_num in range(pdf.getNumPages()):
            page = pdf.getPage(page_num)
            text += page.extractText()
    return text

def predictResume(filename):
    try:
        text = textract.process(filename)
        text = text.decode('utf-8').replace("\\n", " ")
        text = cleanResume(text)
        text = [text]
        text = np.array(text)
        vectorizer = pickle.load(open("vectorizer.pickle", "rb"))
        resume = vectorizer.transform(text)
        model = load('model.joblib')
        result = model.predict(resume)
        labeldict = {
            0: 'Arts',
            1: 'Automation Testing',
            2: 'Operations Manager',
            3: 'DotNet Developer',
            4: 'Civil Engineer',
            5: 'Data Science',
            6: 'Database',
            7: 'DevOps Engineer',
            8: 'Business Analyst',
            9: 'Health and fitness',
            10: 'HR',
            11: 'Electrical Engineering',
            12: 'Java Developer',
            13: 'Mechanical Engineer',
            14: 'Network Security Engineer',
            15: 'Blockchain ',
            16: 'Python Developer',
            17: 'Sales',
            18: 'Testing',
            19: 'Web Designing'
        }
        return labeldict[result[0]]
    except UnicodeDecodeError:
        print('File', filename, 'cannot be extracted for prediction! - skipped')


def find_score(jobdes, filename, customKeywords):
    resume = Preprocessfile(filename)
    customKeywords = ' '.join(customKeywords)
    jobdes = jobdes + ' ' + customKeywords
    text = [resume, jobdes]
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text)
    matchpercent = cosine_similarity(count_matrix)[0][1] * 100
    matchpercent = round(matchpercent, 2)
    return matchpercent

response_data = []

@app.route('/process', methods=['GET', 'POST'])
def process_page():
    if request.method == 'GET':
        try:
            # Retrieve data from the database using SQLAlchemy
            data = ResponseData.query.all()
            response_data = [{'resume_id': item.resume_id, 'score': item.score, 'profile': item.profile, 'user_id': item.user_id,
                              'tags': item.tags, 'job_description': item.job_description} for item in data]

            return jsonify(response_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'POST':
        try:
            my_profile = request.form.get('profile')
            user_id = request.form.get('userId')
            resumes = request.files.getlist('resumes')
            my_tags = request.form.get('tags')
            my_jd = request.form.get('jobDescription')

            for resume in resumes:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(resume.filename))
                resume.save(file_path)

                # Calculate the score
                score = find_score(my_jd, file_path, my_tags)

                # Insert the data into the database using SQLAlchemy
                data = ResponseData(
                    resume_id=resume.filename,
                    score=score,
                    profile=my_profile,
                    user_id=user_id,
                    tags=my_tags,
                    job_description=my_jd
                )

                db.session.add(data)
                db.session.commit()

            return jsonify({'message': 'Data submitted successfully'})

        except Exception as e:
            return jsonify({'error': 'An error occurred while processing the data.'}), 400

    return jsonify({'error': 'Invalid request method.'}), 405

######################################

@app.route('/results', methods=['GET'])
def display_results():
    return jsonify(results_list)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the 'resumes' field is in the request
    if 'resumes' not in request.files:
        return jsonify({'error': 'No resumes provided'}), 400

    uploaded_files = request.files.getlist('resumes')

    # Loop through uploaded files
    file_paths = []
    for file in uploaded_files:
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            file_paths.append(file_path)

    return jsonify({'message': 'Resumes uploaded successfully', 'file_paths': file_paths})

@app.route('/', methods=['GET'])
def index():
    # You can return an HTML template or a simple message here
    return "Welcome to the homepage."
@app.route('/test_db_connection', methods=['GET'])
def test_db_connection():
    try:
        db.session.execute(text('SELECT 1'))
        return 'Database connection successful'
    except Exception as e:
        # Add a debugging print statement
        print("Database connection error:", str(e))
        return 'Database connection failed: ' + str(e)

@app.route('/test_post', methods=['POST'])
def test_post():
    return 'POST request received'

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)

