from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

users = {'mentors': [], 'mentees': []}

@app.route('/')
def index():
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    user_type = request.form.get('user_type')
    user_name = request.form.get('user_name')
    user_skills = request.form.get('user_skills')
    if user_type and user_name and user_skills:
        users[user_type].append({'name': user_name, 'skills': user_skills.split(',')})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
