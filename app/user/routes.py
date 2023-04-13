from app.user import bp
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from ..post.forms import PostForm
from .. import db
from ..models import User, Post, Follow
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


@bp.route('/<int:user_id>/follow', methods=['GET', 'POST'])
@login_required
def follow(user_id):
    # Get the user by id from the database
    user_wer = User.query.get_or_404(user_id)
    wee_wer = Follow.query.filter_by(followee=current_user, follower=user_wer)

    if wee_wer.count() > 0:
        flash('You are already following a user!', category='error')
    else:
        go_follow = Follow(followee=current_user, follower=user_wer)
        db.session.add(go_follow)
        db.session.commit()
        flash('You have followed to a user!', category='success')

    return redirect(request.referrer)


@bp.route('/<int:user_id>/unfollow', methods=['GET', 'POST'])
@login_required
def unfollow(user_id):
    # Get the user by id from the database
    user_wer = User.query.get_or_404(user_id)
    wee_wer = Follow.query.filter_by(followee=current_user, follower=user_wer)

    if wee_wer.count() > 0:
        un_follow = wee_wer.first()
        db.session.delete(un_follow)
        db.session.commit()
        flash('You have unfollowed a user!', category='success')
    else:
        flash('You are already unfollowed from the user!', category='error')

    return redirect(request.referrer)
