from flask import Flask, send_from_directory, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os, datetime

UPLOAD_FOLDER = '/images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'secret-key'

login_manager = LoginManager()
login_manager.init_app(app)

# In-memory store
users = {'user': {'password': 'password'}}
alerts = []

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return
    user = User()
    user.id = username
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    if (username in users and request.form['password'] == users[username]['password']):
        user = User()
        user.id = username
        login_user(user)
        return redirect(url_for('index'))

    return 'Bad login'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'

@app.route('/')
@login_required
def index():
    return '<a href="/logout">Logout</a></br></br>' + '<br>'.join(['<p>{}</p>'.format(a) for a in alerts])

@app.route('/alerts', methods=['GET'])
@login_required
def read_alert():
    image_files = os.listdir(app.config['UPLOAD_FOLDER'])
    image_urls = [request.url_root + 'uploads/' + file for file in image_files]
    return render_template('alerts.html', alerts=alerts, image_urls=image_urls)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() is "png"

@app.route('/alerts', methods=['POST'])
def post_alert():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'message': 'Allowed file type is png'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)