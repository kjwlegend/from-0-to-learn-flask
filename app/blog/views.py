from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for, g, session


# 创建蓝图

bp = Blueprint('blog', __name__, url_prefix='/blog', static_folder='static', template_folder='templates')

# @bp.route('/')
def index():
    posts = [1,2,3,4,5]
    return render_template('index.html',posts=posts)

