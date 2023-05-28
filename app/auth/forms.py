from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from werkzeug.security import check_password_hash
from .models import User



class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20, message='用户名长度在1-20个字符之间')])
    password = PasswordField('密码', validators=[DataRequired(), Length(8, 128, message='密码长度在8-128个字符之间')])
    
    error = None
    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if not user:
            error = '用户名不存在'
            raise ValidationError(error)
        elif user and not check_password_hash(user.password, field.data):
            raise ValidationError('密码错误')
        
class RegisterForm(FlaskForm):
    # 注册表单
    username = StringField('username', validators=[
        DataRequired(message="不能为空"), 
        Length(min=2, max=32, message="超过限制字数！")
        ])
    password = PasswordField('password', validators=[
        DataRequired(message="不能为空"),
        Length(min=2, max=32, message="超过限制字数！"),
        EqualTo('password1', message='两次密码输入不一致！')
        ])
    password1 = PasswordField('password1',validators=[
        DataRequired(message="不能为空"),
        EqualTo('password', message='两次密码输入不一致！')])
    
    def validate_username(form, field):
        user = User.query.filter_by(username=field.data).first()
        if user is not None:
            message = '该用户名称已存在！'
            raise ValidationError(message)