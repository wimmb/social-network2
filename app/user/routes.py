from app.user import bp
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from ..post.forms import PostForm
from .. import db
from ..models import User, Post
from ..user.forms import ProfileForm


@bp.route("/blog")
def blog():
    form = PostForm()
    posts = (
        db.session.query(Post)
        .filter(
            Post.author_id == current_user.id
        )
        .order_by(Post.created_at.desc())
        .all()
    )
    return render_template("user/blog.html", posts=posts, form=form)


@bp.route("/profile/<string:username>", methods=['GET', 'POST'])
@login_required
def profile(username):
    if not current_user.is_authenticated:
        return redirect(url_for("main.index"))

    user = db.session.query(User).filter(User.username == username).first_or_404()

    form = ProfileForm()
    if form.validate_on_submit():
        user.profile.first_name = form.first_name.data
        user.profile.last_name = form.last_name.data
        user.profile.linkedin_url = form.linkedin_url.data
        user.profile.facebook_url = form.facebook_url.data
        user.profile.bio = form.bio.data
        db.session.commit()
        flash('Your changes have been saved.', category="success")
        return redirect(url_for('user.profile', username=user.username))
    elif request.method == 'GET':
        form.first_name.data = user.profile.first_name
        form.last_name.data = user.profile.last_name
        form.linkedin_url.data = user.profile.linkedin_url
        form.facebook_url.data = user.profile.facebook_url
        form.bio.data = user.profile.bio

    context = {
        "title": f"{user.username} - profile",
        "user": user,
        "form": form
    }

    return render_template("user/profile.html", **context)
