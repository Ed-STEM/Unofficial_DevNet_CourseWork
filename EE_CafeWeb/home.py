import functools
from os import urandom
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from markupsafe import escape

from EE_CafeWeb.db import get_db

blueprint_home = Blueprint('home', __name__, url_prefix='/home')

@blueprint_home.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')
	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()

@blueprint_home.route('/', methods=(['GET']))
def home():
    try:
        load_logged_in_user()  #fill out home page for regular user
        return render_template('home/home.html')
    except:
        return render_template('home/home.html') #Generic Welcome page.
    
@blueprint_home.route('/comingsoon', methods=(['GET']))
def comingsoon():
    try:
        return render_template('home/comingsoon.html')
    except:
        return redirect(url_for('home.home'))

@blueprint_home.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None

		if not username:
			error = 'Username is required.'
		elif not password:
			error = 'Password is required.'

		if error is None:
			try:
				db.execute(
					"INSERT INTO user (username, password) VALUES (?, ?)",
					(username, generate_password_hash(password)),
				)
				db.commit()
			except db.IntegrityError:
				error = f"User {username} is already registered."
			else:
				return redirect(url_for("home.login"))

		flash(error)
	return render_template('home/register.html')

@blueprint_home.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		user = db.execute(
			'SELECT * FROM user WHERE username = ?', (username,)
		).fetchone()

		if user is None:
			error = "Incorrect username."
		elif not check_password_hash(user['password'], password):
			error = 'Incorrect password.'

		if error is None:
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('home.login'))
		flash(error)

	return render_template('home/login.html')

@blueprint_home.route('/logout')
def logout():
    session.clear()

    return redirect(url_for('home.home'))

def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:

			return redirect(url_for('home.home'))  

		return view(**kwargs)

	return wrapped_view