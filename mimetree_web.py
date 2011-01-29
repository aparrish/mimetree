#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import os.path
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import uimodules

import urllib

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("facebook_api_key", help="your Facebook application API key")
define("facebook_secret", help="your Facebook application secret")

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/friends.json", FriendsJSONHandler),			
			(r"/auth/login", AuthLoginHandler),
		]
		settings = dict(
			cookie_secret="12oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
			login_url="/auth/login",
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			xsrf_cookies=True,
			facebook_api_key=options.facebook_api_key,
			facebook_secret=options.facebook_secret,
			debug=True,
		)
		tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		user_json = self.get_secure_cookie("user")
		if not user_json: return None
		return tornado.escape.json_decode(user_json)

class MainHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
	@tornado.web.authenticated
	@tornado.web.asynchronous
	def get(self):
		self.render("index.html")

class FriendsJSONHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
	@tornado.web.authenticated
	@tornado.web.asynchronous
	def get(self):
		http = tornado.httpclient.AsyncHTTPClient()
		http.fetch('https://api.facebook.com/method/fql.query?' + \
			urllib.urlencode({'access_token': self.current_user['access_token'],
				'query': 'select uid, first_name, last_name, name, religion, sex, hometown_location, political, current_location, activities, interests, music, tv, movies, books, work_history, education_history from user where uid in (select uid2 from friend where uid1 = me())'}),
			callback=self._on_response)

	def _on_response(self, response):
		logging.error("response %s" % str(response))
		if response.error: raise tornado.web.HTTPError(500)
		self.write(response.body)
		#logging.error(response.body)
		self.finish()

class AuthLoginHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
	@tornado.web.asynchronous
	def get(self):
		if self.get_argument("code", False):
			self.get_authenticated_user(
				redirect_uri='http://resolution.decontextualize.com:8888/auth/login',
				client_id=self.settings["facebook_api_key"],
				client_secret=self.settings["facebook_secret"],
				code=self.get_argument("code"),
				callback=self.async_callback(self._on_login))
			return
		self.authorize_redirect(redirect_uri='http://resolution.decontextualize.com:8888/auth/login',
			client_id=self.settings["facebook_api_key"],
			extra_params={"scope": "user_about_me,user_education_history,user_location,email,friends_about_me,friends_activities,friends_birthday,friends_education_history,friends_events,friends_groups,friends_hometown,friends_interests,friends_likes,friends_location,friends_relationships,friends_relationship_details,friends_religion_politics,friends_status,friends_website,friends_work_history,user_about_me,user_activities,user_birthday,user_education_history,user_events,user_groups,user_hometown,user_interests,user_likes,user_location,user_relationships,user_relationship_details,user_religion_politics,user_status,user_website,user_work_history"})

	def _on_login(self, user):
		logging.error(user)
		self.set_secure_cookie("user", tornado.escape.json_encode(user))
		self.redirect("/")

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
