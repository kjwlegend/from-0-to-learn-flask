from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from werkzeug.security import check_password_hash


class CategoryForm(FlaskForm):
    name = StringField('分类名称', validators=[DataRequired(), Length(1, 20, message='分类名称长度在1-20个字符之间')])
    icon = StringField('图标', validators=[Length(1, 50, message='图标长度在1-20个字符之间')])