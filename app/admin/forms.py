from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from werkzeug.security import check_password_hash
from app.blog.models import Category, Tag, Post, PostPublishType

class CategoryForm(FlaskForm):
    name = StringField('分类名称', validators=[DataRequired(), Length(1, 20, message='分类名称长度在1-20个字符之间')])
    icon = StringField('图标', validators=[Length(1, 50, message='图标长度在1-20个字符之间')])
    
    
class ArticleForm(FlaskForm):
    title = StringField('文章标题', validators=[DataRequired(), Length(1, 50, message='文章标题长度在1-50个字符之间')])
    content = StringField('文章内容', validators=[DataRequired()])
    category = StringField('文章分类', validators=[DataRequired()])
    tag = StringField('文章标签', validators=[DataRequired()])
    # icon = StringField('图标', validators=[Length(1, 50, message='图标长度在1-20个字符之间')])
    
class PostForm(FlaskForm):
    # 添加文章表单
    title = StringField('标题', validators=[
        DataRequired(message="不能为空"), 
        Length(max=128, message="不符合字数要求！")
    ])
    desc = StringField('描述', validators=[
        DataRequired(message="不能为空"), 
        Length(max=200, message="不符合字数要求！")
    ])
    has_type = RadioField('发布状态', 
        choices=(PostPublishType.draft.name, PostPublishType.show.name), 
        default=PostPublishType.show.name)
    category_id = SelectField(
        '分类', 
        choices=None, 
        coerce=int,
        validators=[
            DataRequired(message="不能为空"),
        ]
    )
    content = TextAreaField('文章详情', 
        validators=[DataRequired(message="不能为空")]
    )
    tags = SelectMultipleField('文章标签', choices=None, coerce=int)
    

class TagForm(FlaskForm):
    # 标签表单
    name = StringField('标签', validators=[
        DataRequired(message="不能为空"), 
        Length(max=128, message="不符合字数要求！")
    ])