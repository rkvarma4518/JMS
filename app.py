from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from database.access_db import insert_user, get_all_users
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a random secret key

login_manager = LoginManager(app)
login_manager.login_view = 'login'


def fetch_data_as_dict_list(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    column_names = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    result = []
    for row in rows:
        row_dict = {column_names[i]: row[i] for i in range(1,len(row)) if row[i] is not None}
        result.append(row_dict) 
    conn.close()
    return result

class User(UserMixin):
    def __init__(self, username, password):
        self.id = username  # Use the username as the user ID
        self.username = username
        self.password = password

    def get_id(self):
        return str(self.username)

@login_manager.user_loader
def load_user(user_name):
    users = get_all_users()
    user = next((u for u in users if u['username'] == user_name), None)
    if user:
        return User(user['username'], user['password'])
    return None


# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the sign page
@app.route('/sign')
def sign():
    return render_template('sign.html')

@app.route('/login', methods=['GET', 'POST'])
# @login_required
def login():
    # Implement your login logic here
    # For simplicity, we'll just check if the provided username and password match
    if request.method == 'POST':
        users = get_all_users()
        username = request.form.get('username')
        password = request.form.get('password')
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)

        if user:
            login_user(User(username, password))
            return redirect(url_for('index'))  # Redirect to the index page after successful login
        else:
            return "Invalid username or password."
    else:
        return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
    # return "Logged out successfully!"

# Route for the registration page
@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print('*************************')
    print(data)

    if insert_user(data['name'], data['email'], data['phone'], data['password']):
        print('Registered successfully')
    else:
        print('Registartion failed!')
    # Return a response (you can customize this based on your requirements)
    return render_template('sign.html')


# Route for the FM service page
@app.route('/fm_service')
@login_required
def fm_service():
    data = fetch_data_as_dict_list('jobs.db', 'all_jobs')
    return render_template('fmservice.html', items=data)

# Route for the contact us page
@app.route('/contact_us')
def contact_us():
    return render_template('contactus.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
