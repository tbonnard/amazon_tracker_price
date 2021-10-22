from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Email, URL
from wtforms.fields.html5 import EmailField, URLField


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={'placeholder': "Your name"})
    email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': "Your email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': "Your password"})
    submit = SubmitField('Confirm')


class UserLoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': "Your email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': "Your password"})
    submit = SubmitField('Confirm')


class ItemPriceForm(FlaskForm):
    url = URLField('URL', validators=[DataRequired(), URL()], render_kw={'placeholder': "URL of the amazon product"})
    price_limit = FloatField('Price limit', validators=[DataRequired()], render_kw={'placeholder': "Your limit price"})
    submit = SubmitField('Confirm')
