from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from werkzeug.security import check_password_hash