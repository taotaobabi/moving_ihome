# coding=utf-8

from tornado.web import RequestHandler
from utils.session import Session
import tornado.web
import json
import logging


class BaseHandler(RequestHandler):
    """定义handler基类"""
    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis

    def prepare(self):
    	self.xsrf_token
        if self.request.headers.get("Content-Type","").startswith("application/json"):
        	self.json_args = json.loads(self.request.body)
        else:
        	self.json_args = None
        # print self.json_args		

    def set_default_headers(self):
        self.set_header("Content-type","application/json,charset=UTF-8")

    def initialize(self):
        pass

    def on_finish(self):
        pass

    def write_error(self, status_code,**kwargs):
    	pass
    def get_current_user(self):
    	self.session = Session(self)
    	# logging.debug(self.session.data)
    	return 	self.session.data  

class StaticFileHandler(tornado.web.StaticFileHandler):
	"""重写StaticFileHandler"""
	def __init__(self, *args, **kwargs):
		super(StaticFileHandler,self).__init__(*args, **kwargs)
		self.xsrf_token

