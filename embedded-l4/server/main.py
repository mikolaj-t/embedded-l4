from flask import Flask, send_from_directory, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os, datetime

app = Flask(__name__)

# Assuming the 3rd partition is mounted at /mnt/p3
UPLOAD_FOLDER = '/mnt/p3'

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

app.route('/alerts', methods=['GET'])
@login_required
def read_alert():
    return jsonify({'alerts': alerts}), 200

@app.route('/alerts', methods=['POST'])
def post_alert():
    alert = request.get_json()
    alert['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    alerts.append(alert)
    return jsonify({'message': 'Alert received'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)