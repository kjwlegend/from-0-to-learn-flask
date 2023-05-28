from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, blueprints
from ..auth.views.auth import login_required
from ..blog.models import Category, Tag, Post

bp = blueprints.Blueprint('admin', __name__, url_prefix='/admin', static_folder='static', template_folder='templates')

@bp.route('/')
@login_required
def index():
    return render_template('admin/index.html')

# CRUD for category, tag, post

@bp.route('/category')
@login_required
def category():
    page = request.args.get('page', 1, type=int)
    pagination = Category.query.order_by(-Category.create_time).paginate(page=page, per_page=5, error_out=False)
    category_list = pagination.items
    print(pagination)
    print(category_list)
    return render_template('admin/category.html',
                           category_list = category_list,
                           pagination = pagination)
