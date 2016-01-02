from localsocial import app
from localsocial.decorator.user_decorator import login_required, query_user
from localsocial.decorator.route_decorator import api_endpoint
from localsocial.service import facebook_service, user_service 
from localsocial.model.user_model import User

from flask import redirect, request, session, g

@app.route('/user/login/facebook')
def facebook_login():
	return redirect(facebook_service.get_auth_redirect(app.config["FB_APP_ID"], "http://localhost:5000/login/facebook/callback"))	#Config-itize

@app.route('/user/login/facebook/callback')
def facebook_login_callback():
	if "error" in request.args or "error_code" in request.args:
		redirect("/login/facebook/error")
	else:
		code = request.args["code"]

		access_token = facebook_service.get_access_token(app.config["FB_APP_ID"], app.config["FB_APP_SECRET"], code, "http://localhost:5000/login/facebook/callback")

		logged_in_user = user_service.login_user_facebook(access_token)

		session["user_id"] = logged_in_user.user_id

		return "Created new user"	#TODO Redirect to home page

@app.route("/user/login/facebook/error")
def facebook_login_error():
	return "Error"

@api_endpoint("/user/login", methods=("POST",))
def do_login():
	email = request.form["email"]
	password = request.form["password"]

	try:
		user_id = user_service.login(email, password)
		session["user_id"] = user_id

		return { "success" : True }
	except:
		return { "success" : False }

@api_endpoint("/user/create", methods=("POST",))
def create_user():
	email = request.form["email"]
	phone = request.form.get("phone", None)
	first_name = request.form["first-name"]
	last_name = request.form["last-name"]
	nick_name = request.form.get("nick-name", None)
	portrait = None

	password = request.form["password"]
	confirm_password = request.form["confirm-password"]

	if password != confirm_password:
		return { "success" : False, "reason" : "password" }
	else:
		new_user = User(email, phone, first_name, last_name, nick_name, portrait)

		new_user = user_service.create_new_user(new_user, password)
		session["user_id"] = new_user.user_id

		return { "success" : True }


@api_endpoint('/user/<queried_user_identifier>')
@login_required
@query_user(get_object = True)
def get_user(queried_user_identifier):
	requested_user = g.queried_user

	return requested_user.to_json_dict()
	
@api_endpoint('/user/<queried_user_identifier>/friends', methods=("GET",))
@login_required
@query_user()
def get_friends(queried_user_identifier):
	queried_user_id = g.queried_user_id

	return user_service.get_friends(queried_user_id)

@api_endpoint('/user/me/friends/request', methods=("GET",))
@login_required
def get_friend_requests():
	current_user = g.user

	return user_service.get_friend_requests_pending(current_user.user_id)

@api_endpoint('/user/<queried_user_identifier>/follows', methods=("GET",))
@login_required
@query_user()
def get_followers(queried_user_identifier):
	queried_user_id = g.queried_user_id

	return user_service.get_followers(queried_user_id)

@api_endpoint('/user/<queried_user_identifier>/follows/followers', methods=("GET",))
@login_required
@query_user()
def get_following(queried_user_identifier):
	queried_user_id = g.queried_user_id

	return user_service.get_following(queried_user_id)

@api_endpoint('/user/<queried_user_identifier>/friends/request', methods=("POST",))
@login_required
@query_user(self_check = True)
def create_friend(queried_user_identifier):
	current_user = g.user
	queried_user_id = g.queried_user_id
	
	return user_service.create_friend(current_user.user_id, queried_user_id)

@api_endpoint('/user/<queried_user_identifier>/follows/request', methods=("POST",))
@login_required
@query_user(self_check = True)
def create_follow(queried_user_identifier):
	current_user = g.user
	queried_user_id = g.queried_user_id

	return user_service.create_follow(current_user.user_id, queried_user_id)