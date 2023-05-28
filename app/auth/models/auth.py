from RealProject import db
from datetime import datetime


class BaseModel(db.Model):
    """基类模型"""
    
    __abstract__ = True
    
    create_time = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 更新时间
    

class User(BaseModel):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)  # 用户名
    password = db.Column(db.String(128), nullable=False)  # 密码
    avatar = db.Column(db.String(128))  # 头像
    is_super_user = db.Column(db.Boolean, default=False)  # 是否是超级管理员
    is_active = db.Column(db.Boolean, default=True)  # 是否激活
    is_staff = db.Column(db.Boolean, default=False)  # 是否是员工
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    