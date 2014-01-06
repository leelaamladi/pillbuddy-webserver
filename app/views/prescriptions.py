from flask import session, render_template, redirect, url_for, request, flash
from app.utils import login_required, get_http_method
from app import app, bcrypt, models
from app.models import User, Follower, Prescription

# Single prescription page
@app.route('/prescriptions/<id>', methods=['GET','POST'])
@login_required
def prescription(id):
	http_method = get_http_method(request)
	if http_method == 'GET':
		id = int(id)
		user = User.objects.get(username=session['logged_in'])
		data = user.prescriptions[id].to_dict()
		return render_template('prescription.html', prescription=data, id=id)
	elif http_method == 'POST': 
		id = int(id)
		new_first_name = request.form['name']
		new_amount = request.form['amount']
		new_doctor = request.form['doctor']
		new_description = request.form['description']

		if 'morningalarm' in request.form and request.form['morningalarm']=='on':
			new_morningalarm = True
		else:
			new_morningalarm = False
		if 'afternoonalarm' in request.form  and request.form['afternoonalarm']=='on':
			new_afternoonalarm = True
		else:
			new_afternoonalarm = False
		if 'eveningalarm' in request.form  and request.form['eveningalarm']=='on':
			new_eveningalarm = True
		else:
			new_eveningalarm = False	
		if 'nightalarm' in request.form  and request.form['nightalarm']=='on':
			new_nightalarm = True
		else:
			new_nightalarm = False	

		user = User.objects.get(username=session['logged_in'])
		prescription=user.prescriptions[id]
		# update prescription
		prescription.name = new_first_name
		prescription.amount = new_amount
		prescription.doctor = new_doctor
		prescription.description = new_description
		prescription.morningalarm = new_morningalarm
		prescription.afternoonalarm = new_afternoonalarm
		prescription.eveningalarm = new_eveningalarm
		prescription.nightalarm = new_nightalarm
		user.save()
		
		flash('Prescription settings successfully changed')
		return redirect(url_for('prescription', id=id))
	else: # if http_method = 'DELETE'
		id = int(id)
		user = User.objects.get(username=session['logged_in'])
		# validate id
		if id >= len(user.prescriptions) or id < 0:
			flash('Prescription ID invalid')
			return redirect(url_for('prescriptions'))
		# delete follower
		user.prescriptions.pop(id)
		user.save()
		
		flash('Prescription removed')
		return redirect(url_for('prescriptions'))


# All prescriptions page
@app.route('/prescriptions', methods=['GET', 'POST'])
@login_required
def prescriptions():
	http_method = get_http_method(request)
	if http_method == 'GET':
		user = User.objects.get(username=session['logged_in'])
		data = []
		for prescription in user.prescriptions:
			data.append(prescription.to_dict())
		return render_template('prescriptions.html', data=data)
	else: # http_method == 'POST'
		new_prescription = Prescription()
		user = User.objects.get(username=session['logged_in'])
		user.prescriptions.append(new_prescription)
		id = len(user.prescriptions)-1
		user.save()
		return redirect(url_for('prescription', id=id))


