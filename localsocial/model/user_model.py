class User():
	def __init__(self, f_name, l_name, n_name, portrait, access_token, access_secret, platform, plat_id):
		self.user_id = -1
		self.first_name = f_name
		self.last_name = l_name
		self.nick_name = n_name
		self.portrait = portrait

		self.access_token = access_token
		self.access_secret = access_secret
		self.login_platform = platform
		self.platform_id = plat_id

	@property
	def full_name(self):
		return self.first_name + " " + self.last_name

	def to_json_dict(self):
		return { "firstName" : self.first_name,
			"lastName" : self.last_name,
			"nickName" : self.nick_name,
			"portrait" : self.portrait,
			"platform" : self.login_platform }