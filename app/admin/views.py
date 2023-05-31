from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, blueprints
from ..auth.views.auth import login_required
from ..blog.models import Category, Tag, Post
from .forms import CategoryForm
from RealProject import db

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

@bp.route('/category/add', methods=['GET', 'POST'])
@login_required
def category_add():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, icon=form.icon.data)
        db.session.add(category)
        db.session.commit()
        flash('分类添加成功')
        return redirect(url_for('admin.category'))

    return render_template('admin/category_form.html', form=form)

@bp.route('/category/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def category_edit(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        category.icon = form.icon.data
        db.session.commit()
        flash('分类编辑成功')
        return redirect(url_for('admin.category'))

    form.name.data = category.name
    form.icon.data = category.icon
    return render_template('admin/category_form.html', form=form)