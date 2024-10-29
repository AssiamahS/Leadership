from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = {'mentors': [], 'mentees': []}
matches = []

@app.route('/')
def index():
    return render_template('index.html', users=users, matches=matches)

@app.route('/add_user', methods=['POST'])
def add_user():
    user_type = request.form.get('user_type')
    user_name = request.form.get('user_name')
    user_skills = request.form.get('user_skills')
    if user_type and user_name and user_skills:
        skills = user_skills.split(',')
        users[user_type].append({'name': user_name, 'skills': skills})
        if user_type == 'mentees':
            for mentor in users['mentors']:
                if any(skill in mentor['skills'] for skill in skills):
                    matches.append({'mentor': mentor['name'], 'mentee': user_name, 'shared_skills': list(set(mentor['skills']) & set(skills))})
    return redirect(url_for('index'))

@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
