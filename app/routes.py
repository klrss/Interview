from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from app import app, db
from datetime import datetime
from app.forms import LoginForm, RegistrationForm, InterviewForm, QuestionForm, CategoryForm
from app.models import User, Role, Interview, Questionary, Category


@app.route('/')
@app.route('/index')
@login_required  # this decorator save function from view anonymous user
def index():
    interviews = Interview.query.order_by(Interview.date.desc()).all()
    users = User.query.all()

    return render_template('index.html', title='Home', interviews=interviews, users=users,
                           current_time=datetime.utcnow())


# admin
@app.route('/foradmin')
@login_required
def foradmin():
    return render_template('foradmin.html')


# login function
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


# logout function
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# register function
@login_required
@app.route('/register', methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #   return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data,
                    email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# create interview function
@app.route('/event', methods=['GET', 'POST'])
def create_interview():
    form = InterviewForm()
    if form.validate_on_submit():
        interview = Interview(title=form.title.data, candidate=form.candidate.data, date=form.date.data,
                              users=form.user.data)
        db.session.add(interview)
        db.session.commit()
        flash('You have created the interview!')
        return redirect(url_for('index'))
    return render_template('interview.html', title='Interview', form=form)


# @app.route('/expertpage/<int:id>')
# @login_required
# def expert_page(id):
#    user = User.query.filter_by(id=id).first_or_404()
#    interviews=Interview.query.filter_by()
#    return render_template('expertpage.html', user=user)

# Questionaryome
@app.route('/quest',methods=['POST','GET'])
@login_required
def quest():
    form_cat = CategoryForm()
    form = QuestionForm()
    if form.validate_on_submit():
        category = Category(name=form_cat.name.data)
        question = Questionary(category=form.category.data, name=form.name.data)
        db.session.add(category)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('foradmin'))
    return render_template('quest.html', form_cat=form_cat, form=form)

    return render_template('quest.html')


if __name__ == '__main__':
    app.run(debug=True)
