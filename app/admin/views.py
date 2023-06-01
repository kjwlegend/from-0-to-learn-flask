from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, blueprints
from ..auth.views.auth import login_required
from ..blog.models import Category, Tag, Post
from .forms import CategoryForm, PostForm, TagForm
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

    return render_template('admin/category_form.html', form=form, id = 0)

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
    return render_template('admin/category_form.html', form=form, id=id)

# 删除分类
@bp.route('/category/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def category_delete(id):
    category = Category.query.get_or_404(id)
    if category.posts.count() > 0:
        flash('该分类下有文章，不能删除')
        return redirect(url_for('admin.category'))
    else:
        db.session.delete(category)
        db.session.commit()
        flash('{}类删除成功'.format(category.name))
        return redirect(url_for('admin.category'))


# 文章管理 : 增删改查

@bp.route('/article')
@login_required
def article():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(-Post.create_time).paginate(page=page, per_page=5, error_out=False)
    article_list = pagination.items
    return render_template('admin/article.html',
                           post_list = article_list,
                           pagination = pagination)


@bp.route('/article/add', methods=['GET', 'POST'])
@login_required
def article_add():
    form = PostForm()
    form.category_id.choices = [ (v.id, v.name) for v in Category.query.all() ]
    form.tags.choices = [ (v.id, v.name) for v in Tag.query.all() ]
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    desc=form.desc.data,
                    has_type=form.has_type.data,
                    category_id=int(form.category_id.data),
                    content=form.content.data
        )
        post.tags =  [ Tag.query.get(tag_id) for tag_id in form.tags.data ]
        db.session.add(post)
        db.session.commit()
        flash(f'{form.title.data}文章添加成功')
        return redirect(url_for('admin.article'))
    
    return render_template('admin/article_form.html', form=form, id = 0)

@bp.route('/article/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def article_edit(post_id):
    # 修改文章
    post = Post.query.get(post_id)
    tags = [tag.id for tag in post.tags]
    form = PostForm(
        title=post.title, desc=post.desc, 
        category_id=post.category.id, has_type=post.has_type.value,
        content=post.content, tags=tags
    )

    form.category_id.choices = [(v.id,v.name) for v in Category.query.all()]
    form.tags.choices = [(v.id,v.name) for v in Tag.query.all()]

    if form.validate_on_submit():
        post.title = form.title.data
        post.desc = form.desc.data
        post.has_type = form.has_type.data
        post.category_id=int(form.category_id.data)
        post.content = form.content.data
        post.tags = [Tag.query.get(tag_id) for tag_id in form.tags.data]
        db.session.add(post)
        db.session.commit()
        flash(f'{form.title.data}文章修改成功')
        return redirect(url_for('admin.article'))
    return render_template('admin/article_form.html', form=form)


@bp.route('/article/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def article_del(post_id):
    # 删除文章
    post = Post.query.get(post_id)
    if post:  
        db.session.delete(post)
        db.session.commit()
        flash(f'{post.title}文章删除成功')
        return redirect(url_for('admin.article'))
    

@bp.route('/tag')
@login_required
def tag():
    # 查看标签列表
    page = request.args.get('page', 1, type=int)
    pagination = Tag.query.order_by(-Tag.create_time).paginate(page=page, per_page=10, error_out=False)
    tag_list = pagination.items
    return render_template('admin/tag.html', tag_list=tag_list, pagination=pagination)


@bp.route('/tag/add', methods=['GET', 'POST'])
@login_required
def tag_add():
    # 增加标签
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(name=form.name.data)
        db.session.add(tag)
        db.session.commit()
        flash(f'{form.name.data}添加成功')
        return redirect(url_for('admin.tag'))
    return render_template('admin/tag_form.html', form=form)


@bp.route('/tag/edit/<int:tag_id>', methods=['GET', 'POST'])
@login_required
def tag_edit(tag_id):
    # 修改标签
    tag = Tag.query.get(tag_id)
    form = TagForm(name=tag.name)
    if form.validate_on_submit():
        tag.name = form.name.data
        db.session.add(tag)
        db.session.commit()
        flash(f'{form.name.data}添加成功')
        return redirect(url_for('admin.tag'))
    return render_template('admin/tag_form.html', form=form)


@bp.route('/tag/del/<int:tag_id>', methods=['GET', 'POST'])
@login_required
def tag_del(tag_id):
    # 删除标签
    tag = Tag.query.get(tag_id)
    if tag:
        db.session.delete(tag)
        db.session.commit()
        flash(f'{tag.name}删除成功')
        return redirect(url_for('admin.tag'))