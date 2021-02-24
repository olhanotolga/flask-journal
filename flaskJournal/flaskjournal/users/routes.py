from flask import Blueprint, redirect, render_template, flash, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from flaskjournal import db, bcrypt
from flaskjournal.models import User, Post
from flaskjournal.users.forms import RegistrationForm, LoginForm, UpdateProfileForm, RequestResetForm, ResetPasswordForm
from flaskjournal.users.utils import send_reset_email, save_picture

# Blueprint function creates a blueprint, calling it creates an instance
users = Blueprint('users', __name__)


# test_user123 test_user123@test.com testtest
# oh test@test.com 12345
# admin667 admin@admin.net adminpw
# 4cats cats@email.com 4cats2frogs
# olhanotolga olhanotolga@gmail.com olha4
# aj ajnochka@gmail.com ajajaj



@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created, you can now log in!', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title='Register', form = form)

@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Login unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Log in', form = form)

@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))

@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	form = UpdateProfileForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your profile info has been updated', 'success')
		return redirect(url_for('users.profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('profile.html', title='Profile', image_file=image_file, form=form)

@users.route('/user/<string:username>')
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user)\
		.order_by(Post.date_posted.desc())\
		.paginate(page=page, per_page=7)
	h1_text = f"Posts by {user.username} ({posts.total})"
	return render_template('user_posts.html', posts=posts, h1=h1_text, user=user)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password', 'info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html', title='Reset password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('Invalid or expired token', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Your password has been updated, you can now log in!', 'success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title='Reset password', form=form)