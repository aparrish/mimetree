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

import urllib
import json
import redis
import bsoup_parse
import mateman

from BeautifulSoup import BeautifulStoneSoup

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("facebook_api_key", help="your Facebook application API key")
define("facebook_secret", help="your Facebook application secret")
define("redis_host", help="hostname for redis", default="localhost", type=str)
define("redis_port", help="port number for redis", default=6379, type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/friends.json", FriendsJSONHandler),			
			(r"/auth/login", AuthLoginHandler),
			(r"/stats.json", StatsHandler)
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
	def get_redis_conn(self):
		return redis.Redis(host=options.redis_host, port=options.redis_port, db=0)
	def get_graph_data(self):
		r = self.get_redis_conn()
		key = "%s:friends" % (self.current_user['access_token'])
		data = r.get(key)
		if data:
			logging.info('got data from cache')
			return data
		else:
			logging.info('cache miss')
			http = tornado.httpclient.HTTPClient()
			response = http.fetch('https://api.facebook.com/method/fql.query?' + \
				urllib.urlencode({'access_token': self.current_user['access_token'],
					'query': 'select uid, first_name, last_name, sex, current_location, activities, interests, music, tv, movies, books, work_history, education_history from user where uid in (select uid2 from friend where uid1 = me()) order by rand() limit 200'}), request_timeout=120.0)
			logging.info("response %s" % str(response))
			if response.error:
				return None
			soup = BeautifulStoneSoup(response.body)
			if soup.find('error_code'):
				return None
			rawjson = json.dumps(bsoup_parse.parse_soup(soup))
			logging.info('setting cache key')
			r.setex(key, rawjson, 86400)
			# clear graph stats if we've freshly loaded friends
			r.delete("%s:graph_stats" % self.current_user['access_token'])
			return rawjson

	def get_graph_stats(self):
		r = self.get_redis_conn()
		key = "%s:graph_stats" % (self.current_user['access_token'])
		data = r.get(key)
		if data:
			logging.info('got graph stats from cache')
			return json.loads(data)
		else:
			logging.info('graph stats cache miss')
			friend_stats = self.get_graph_data()
			friend_data = json.loads(friend_stats)
			crunched = mateman.crunchNumbers(friend_data)
			r.setex(key, json.dumps(crunched), 86400)
			return crunched

class MainHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
	@tornado.web.authenticated
	def get(self):
		self.render("index.html")

class StatsHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
	@tornado.web.authenticated
	def get(self):
		friends = json.loads(self.get_graph_data())
		stats = self.get_graph_stats()
		fbid = self.get_argument("uid", None)
		if fbid:
			if fbid not in friends:
				raise tornado.web.HTTPError(404)
			logging.info("user: %s" % str(friends[fbid]))
			logging.info("stats: %s (%s)" % (str(stats), str(type(stats))))
			self.set_header('Content-Type', 'application/json')
			self.write(json.dumps(mateman.getStats(friends[fbid], stats)))
		else:
			raise tornado.web.HTTPError(400)
		

class FriendsJSONHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
	@tornado.web.authenticated
	def get(self):
		self.set_header('Content-Type', 'application/json')
		rawjson = self.get_graph_data()
		if rawjson is None:
			# couldn't get json, probably auth problem
			self.redirect('/auth/login')
		self.write(rawjson)

class AuthLoginHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
	@tornado.web.asynchronous
	def get(self):
		if self.get_argument("code", False):
			self.get_authenticated_user(
				redirect_uri='http://resolution.decontextualize.com:%d/auth/login' % options.port,
				client_id=self.settings["facebook_api_key"],
				client_secret=self.settings["facebook_secret"],
				code=self.get_argument("code"),
				callback=self.async_callback(self._on_login))
			return
		self.authorize_redirect(redirect_uri='http://resolution.decontextualize.com:%d/auth/login' % options.port,
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
