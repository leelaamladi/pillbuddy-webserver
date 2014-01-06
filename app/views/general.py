from flask import session, render_template, redirect, url_for, request, flash
from app.utils import login_required, get_http_method
from app import app, bcrypt, models
from app.models import User, Follower, Prescription

# Home page
@app.route('/', methods=['GET'])
def home():
	# If user not logged in, render home template
	if 'logged_in' not in session:
		return render_template('home.html')
	else:
		user = User.objects.get(username=session['logged_in'])
		# group user presecriptions by alarm
		morning = []
		afternoon = []
		evening = []
		night = []
		for id,p in enumerate(user.prescriptions):
			values = p.time_sort()
			values['id'] = id
			# sorts prescriptions into arrays based on bool values of alarms
			if p.morningalarm:
				morning.append(values)	
			if p.afternoonalarm:
				afternoon.append(values)
			if p.eveningalarm:
				evening.append(values)
			if p.nightalarm:
				night.append(values)
		data = {
			'morning': morning,
			'afternoon': afternoon,
			'evening': evening, 
			'night': night
		}
		return render_template('dashboard.html', data=data)

# Settings
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
	http_method = get_http_method(request)
	if http_method == 'POST':
		new_username = request.form['username']
		#new_password = request.form['password']
		new_first_name = request.form['first_name']
		new_last_name = request.form['last_name']
		new_email = request.form['email']
		new_phone = request.form['phone']

		user = User.objects.get(username=session['logged_in'])
		user.username = new_username
		#user.password = bcrypt.generate_password_hash(new_password)
		user.first_name = new_first_name
		user.last_name = new_last_name
		user.email = new_email
		user.phone = new_phone
		user.save()

		flash('Settings successfully changed')
		return redirect(url_for('settings'))
	else: # if http_method='GET'
		user = User.objects.get(username=session['logged_in'])
		data = user.to_dict()
		return render_template('settings.html', data=data)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
	http_method = get_http_method(request)
	if http_method == 'POST':
		username = request.form['username']
		password = request.form['password']
		first_name = request.form['firstname']
		last_name = request.form['lastname']
		email = request.form['email']
		errors = []
		if len(username) > 25:
			errors.append('Username must be less than 25 characters')
		if len(email) > 40 :
			errors.append('Email must be less than 40 characters')
		if len(first_name) > 25 :
			errors.append('First name must be less than 25 characters')
		if len(last_name) > 25 :
			errors.append('Last name must be less than 25 characters')
		if len(errors) > 0:
			flash(errors)
			return redirect(url_for('register'))
		# generate password hash
		pw_hash = bcrypt.generate_password_hash(password)

		# create new user
		newuser = User(username=username, password=pw_hash, first_name=first_name, last_name=last_name, email=email)
		newuser.save()
		
		# log user in
		session['logged_in'] = username
		
		return redirect(url_for('home'))
	
	else: # if http_method='GET'
		return render_template('register.html')

# Login Route
@app.route('/login', methods=['POST'])
def login():
	username = request.form['username']
	password = request.form['password']
	user = User.objects.get(username=username)
	
	# if user not in db, redirect to home
	if user == None:
		flash('Username invalid')
		return redirect(url_for('home'))
	else:
		# username valid, check password against hashed password in db
		if bcrypt.check_password_hash(user.password, password):
			# add username to session
			session['logged_in'] = username
			return redirect(url_for('home'))
		# if password invalid
		else:
			flash('Invalid Username/Password match')
			return redirect(url_for('home'))

# Log out
@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('home'))
