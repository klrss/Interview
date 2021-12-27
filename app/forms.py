from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateTimeField
from wtforms import SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Role, Interview


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    # role list for choice in SelectedField
    role = SelectField('Role', coerce=int)
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def __init__(self, *args,**kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different name.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class InterviewForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    candidate = StringField('Candidate', validators=[DataRequired()])
    user = SelectMultipleField('User', coerce=int)
    date = DateTimeField(format='%Y-%m-%d %H:%M',default=datetime.today())
    submit = SubmitField('Create Interview')

    def __init__(self, *args,**kwargs):
        super(InterviewForm, self).__init__(*args, **kwargs)
        self.user.choices = [(user.id,'{} {}'.format(user.firstname,user.lastname))
                             for user in User.query.order_by(User.firstname).all()]

