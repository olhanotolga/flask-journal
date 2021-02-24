import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flaskjournal import app, mail

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

	output_size = (256, 256)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	
	return picture_fn


def send_reset_email(user):
	token = user.get_reset_token()
	# always better to send an actual email address domain in the sender field:
	msg = Message('Password reset requested', sender='olhanotolga@gmail.com', recipients=[user.email])
	# _external=True - absolute URL instead of a relative one (for link in the email)
	msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email. No changes will be made.
'''
	mail.send(msg)