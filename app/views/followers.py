from flask import session, render_template, redirect, url_for, request, flash
from app.utils import login_required, get_http_method
from app import app, bcrypt, models
from app.models import User, Follower, Prescription

@app.route('/followers/new', methods=['GET', 'POST'])
@login_required
def new_follower():
	http_method = get_http_method(request)
	if http_method == 'POST':
		email = request.form['email']
		phonenumber = request.form['phonenumber']
		twitter = request.form['twitter']
		if 'email_on' in request.form and request.form['email_on']=='on':
			email_on = True
		else:
			email_on = False
		if 'phone_on' in request.form  and request.form['phone_on']=='on':
			phone_on = True
		else:
			phone_on = False
		if 'twitter_on' in request.form  and request.form['twitter_on']=='on':
			twitter_on = True
		else:
			twitter_on = False

		user = User.objects.get(username=session['logged_in'])
		newfollower = Follower(email=email, phonenumber=phonenumber, twitter=twitter, email_on=email_on, phone_on=phone_on, twitter_on=twitter_on)
		user.followers.append(newfollower)
		user.save()

		flash('New Follower Added')
		return redirect(url_for('followers'))
	
	else: # if http_method='GET'
		return render_template('addfollower.html')

# Followers page
@app.route('/followers', methods=['GET'])
@login_required
def followers():
	user = User.objects.get(username=session['logged_in'])
	data = []
	for follower in user.followers:
		data.append(follower.to_dict())
	return render_template('followers.html', data=data)

@app.route('/followers/<id>', methods=['GET','POST','DELETE'])
@login_required
def follower(id):
	http_method = get_http_method(request)
	if http_method == 'GET':
		return redirect(url_for('followers'))
	
	elif http_method == 'POST':
		id = int(id)
		new_email = request.form['email']
		new_phonenumber = request.form['phonenumber']
		new_twitter = request.form['twitter']
		
		if 'email_on' in request.form :
			new_email_status = True
		else:
			new_email_status = False
		if 'phone_on' in request.form :
			new_phonenumber_status = True
		else:
			new_phonenumber_status = False
		if 'twitter_on' in request.form :
			new_twitter_status = True
		else:
			new_twitter_status = False	

		user = User.objects.get(username=session['logged_in'])
		follower=user.followers[id]
		follower.email = new_email
		follower.phonenumber = new_phonenumber
		follower.twitter = new_twitter
		follower.email_on = new_email_status
		follower.phone_on = new_phonenumber_status
		follower.twitter_on = new_twitter_status
		user.save()

		flash('Follower settings successfully changed')
		return redirect(url_for('followers'))
	else: # if http_method='DELETE'
		id = int(id)
		user = User.objects.get(username=session['logged_in'])
		# validate id
		if id >= len(user.followers) or id < 0:
			flash('Follower ID invalid')
			return redirect(url_for('followers'))
		# delete follower
		user.followers.pop(id)
		user.save()
		
		flash('Follower removed')
		return redirect(url_for('followers'))