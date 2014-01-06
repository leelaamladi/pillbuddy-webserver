# Misc. Helper Functions
from functools import wraps #for login_required
from flask import session

"""If user isn't logged in, they will be redirected away from 
certain pages back to home"""
def login_required(f):
	@wraps(f)
	def is_logged_in(*args, **kwargs):
		if 'logged_in' not in session:
			return redirect(url_for('home'))
		return f(*args, **kwargs)
 	return is_logged_in

""" Returns the desired http method.
	Looks for a _method=DELETE property in the form"""
def get_http_method(request):
	if request.method == 'POST' and '_method' in request.form and request.form['_method']=='DELETE':
		return 'DELETE'
	else:
		return request.method