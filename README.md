# Pillbuddy-Webserver
A Flask web application to connect users with the Pillbuddy box.
The server is currently live at http://dry-lowlands-1091.herokuapp.com

## Running the App
To run the server, enter `python run.py` in the terminal. The web app can be accessed at `http://localhost:3000`

## Todos:
- Fix bugs in Settings page:
	- fix bug where values are not rendered in form on settings page.
	- when updating settings, only save values which have differed, and are valid
	- if the username is changed, change the username value stored in session storage
- Add url endpoints for pillbox
	- url for registering a pillbox serial number with a user
	- url to be used by pillbox to report whether pills were taken or not
- Clean up CSS styling


## Future features
- Add feature for logging when pills were taken
	- create new db model for a 'log' with necessary properties 
	- Log model should NOT be an embedded document list in a User, it should be a collection of its own
	- create url endpoint for viewing logs in a neat way (table? calendar?)
- Upgrade followers to users
	- two levels of permissions for user data
		- followers of a user have read-only access to prescriptions and logs, but can remove themselves as a follower.
	- add 'Following' page so user can see which users he/she is following
