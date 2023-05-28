import functools
from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, g, session
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from RealProject import db
from ..forms import LoginForm, RegisterForm

# 创建蓝图

bp = Blueprint('auth', __name__, url_prefix='/auth', static_folder='../static', template_folder='../templates')


@bp.before_app_request
def load_logged_in_user():
    # 检查用户id是否存在
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        # 查询用户信息
        g.user = User.query.filter_by(id=user_id).first()

@bp.route('/login', methods=('GET', 'POST'))
def login():
    # 登录视图
    form = LoginForm()
    redirect_to = request.args.get('next')
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        session.clear()
        session['user_id'] = user.id
        if redirect_to is not None:
            return redirect(redirect_to)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User(username=username, password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
    
        # 注册成功, 跳转到登录页面
        session.clear()
        session['user_id'] = user.id
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@bp.route('/logout')
def logout():
    # 注销
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    # 登录装饰器
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            redirect_to = f"{url_for('auth.login')}?next={request.path}"
            return redirect(redirect_to)
        return view(**kwargs)
    return wrapped_view