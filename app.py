from flask import Flask, render_template, redirect, url_for, request, session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
 
import pymysql
pymysql.install_as_MySQLdb()
 
# Initialize the Flask app
app = Flask(__name__)
 
# Set the secret key for session management
app.secret_key = 'your_secret_key_here'
 
# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:srividya@database-1.czeyckoc6yva.us-east-1.rds.amazonaws.com:3306/ajabenchdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
# Initialize the SQLAlchemy object
db = SQLAlchemy(app)
 
# Create a User model to store user credentials
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
 
    def __repr__(self):
        return f'<User {self.username}>'
 
# Create the database tables (run this only once)
with app.app_context():
    db.create_all()
 
# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
 
# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Query the database to check if the user exists
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return "Invalid credentials, please try again."
    return render_template('login.html')
 
# Home route (after successful login)
@app.route('/')
@login_required
def home():
    return render_template('index.html')
 
# Route to logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))
 
# Run the application
if __name__ == '__main__':
    app.run(debug=True)