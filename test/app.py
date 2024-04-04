from flask import Flask, render_template, request, redirect, url_for, session
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

users = {
    'admin': {'password': 'admin', 'email': 'admin@example.com', 'age': 30, 'userid': 1},
    'user1': {'password': 'password1', 'email': 'user1@example.com', 'age': 25, 'userid': 2},
    'user2': {'password': 'password2', 'email': 'user2@example.com', 'age': 28, 'userid': 3},
    'user3': {'password': 'password3', 'email': 'user3@example.com', 'age': 32, 'userid': 4},
    'user4': {'password': 'password4', 'email': 'user4@example.com', 'age': 22, 'userid': 5},
    'user5': {'password': 'password5', 'email': 'user5@example.com', 'age': 35, 'userid': 6}
}


@app.route('/')
def home():
    return render_template('index.html')

import re

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        age = int(request.form['age'])

        # Validate username, password, and confirm_password
        if len(username) < 6:
            return render_template('register.html', error='Username must be at least 6 characters long')
        if len(password) < 6 or not re.search(r"[A-Z]", password) or not re.search(r"\d", password):
            return render_template('register.html', error='Password must be at least 6 characters long and contain at least 1 capitalized letter and 1 number')
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')

        # Assign user ID based on the current number of users
        userid = len(users) + 1
        # Add user to dictionary
        users[username] = {'password': password, 'email': email, 'age': age, 'userid': userid}
        return redirect(url_for('login'))
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('user_page'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/user_page')
def user_page():
    if 'username' in session:
        return render_template('user_page.html', users=users)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
