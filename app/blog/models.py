# 创建数据库分类
from RealProject import db
from datetime import datetime
from sqlalchemy.dialects.mysql import LONGTEXT
from enum import IntEnum


class BaseModel(db.Model):
    # 基类模型
    __abstract__ = True

    create_time = db.Column(db.DateTime, default=datetime.now) # 创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now) # 更新时间

class Category(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    # 一对多关系
    # posts = db.relationship('Post', back_populates='category')
    posts = db.relationship('Post', backref='category', lazy='dynamic')
    icon = db.Column(db.String(50))

    
    def __repr__(self):
        return '<Category {}>'.format(self.name)
    
class PostPublishType(IntEnum):
    draft = 0 # 草稿
    show = 1 # 展示
    
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)


class Post(BaseModel):
    # 文章模型
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    desc = db.Column(db.String(200))
    content = db.Column(LONGTEXT, nullable=False)
    has_type = db.Column(db.Enum(PostPublishType), default=PostPublishType.show, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    #多对多关系
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('post', lazy=True))
    
    def __repr__(self):
        return '<Post {}>'.format(self.title)



class Tag(BaseModel):
    """ 文章标签
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<Tag {self.name}>'
