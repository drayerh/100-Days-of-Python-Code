from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import os

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize the database and migration manager
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize the login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    """
    User model for storing user details.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Task(db.Model):
    """
    Task model for storing task details.
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    priority = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<Task {self.id}>'

@login_manager.user_loader
def load_user(user_id):
    """
    Load user by ID.
    """
    return User.query.get(int(user_id))

with app.app_context():
    # Create all database tables
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a new user.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log in an existing user.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Login failed. Check your username and/or password.', 'danger')
        return redirect(url_for('register'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """
    Log out the current user.
    """
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """
    Display and add tasks for the current user.
    """
    if request.method == 'POST':
        task_content = request.form['content']
        task_priority = request.form['priority']
        if task_content.strip():
            new_task = Task(content=task_content, user_id=current_user.id, priority=task_priority)
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.priority.desc(), Task.created_at).all()
    return render_template('index.html', tasks=tasks)

@app.route('/complete/<int:id>')
@login_required
def complete(id):
    """
    Mark a task as complete or incomplete.
    """
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        return redirect('/')
    task.completed = not task.completed
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """
    Edit an existing task.
    """
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        return redirect('/')
    if request.method == 'POST':
        task.content = request.form['content']
        task.priority = request.form['priority']
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', task=task)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    """
    Delete an existing task.
    """
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        return redirect('/')
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)