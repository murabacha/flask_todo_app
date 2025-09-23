from flask import render_template, redirect, url_for, flash, request
from todo_app import app, db, bcrypt
from todo_app.models import Todo,User
from todo_app.forms import TodoForm,RegistrationForm, LoginForm
from flask_login import login_required, current_user, login_user, logout_user,LoginManager
 
 
login_manager = LoginManager(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/home')
@login_required
def index():
    todos = Todo.query.filter_by(owner=current_user).all()
    return render_template('index.html' , todos=todos)

@app.route('/todo', methods=['GET', 'POST'])
def add_todo():
    form = TodoForm()
    if form.validate_on_submit():
        todo = Todo(title=form.title.data, description=form.description.data, date_ending=form.date_ending.data, user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
        flash('Your todo has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('add_todo.html',title='Add Todo', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/delete')
@login_required
def delete():
    todo = Todo.query.get(request.args.get('id'))
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))