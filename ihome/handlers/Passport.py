# coding=utf-8

import logging
import hashlib
import config

from datetime import datetime
from .BaseHandler import BaseHandler
from utils.response_code import RET
from utils.session import Session
from utils.common import require_logined


class RegisterHandler(BaseHandler):

	def post(self):
		mobile = self.json_args.get("mobile")
		phoneCode = self.json_args.get("phonecode")
		passwd = self.json_args.get("password")
		imagecode = self.json_args.get("imagecode")
		imagecodeid = self.json_args.get("imagecodeid")
		# logging.debug(mobile)
		# logging.debug(phoneCode)
		# logging.debug(passwd)
		# logging.debug(imagecodeid)
		# logging.debug(imagecode)
		if not all((mobile,phoneCode,passwd,imagecode,imagecodeid)):
			return self.write({"errno":RET.PARAMERR, "errmsg":"参数错误"})
		try:
			real_imagecode = self.redis.get("image_code_%s" % imagecodeid)
			logging.debug(real_imagecode)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errno=RET.DBERR, errmsg="查询出错"))
		if real_imagecode.lower() != imagecode.lower():
			return self.write(dict(errno="4000", errmsg="验证码已过期！"))
		try:
			real_phonecode = self.redis.get("sms_code_%s" % mobile)
			# logging.debug(real_phonecode)
		except Exception as e:
			logging.error(e)
			self.write(dict(errno=RET.DBERR, errmsg="查询出错"))
		else:
			if not real_phonecode:
				return self.write(dict(errno=RET.NODATA, errmsg="验证码已过期！"))
			if real_phonecode != phoneCode:
				return self.write(dict(errno=RET.DATAERR, errmsg="验证码填写错误！"))
		passwd = hashlib.sha256(config.passwd_hash_key+passwd).hexdigest()    
		try:
			sql = "insert into ih_user_profile(up_name,up_mobile,up_passwd) values(%(name)s,%(mobile)s,%(passwd)s)"
			ret = self.db.execute(sql, name=mobile, mobile=mobile, passwd=passwd)
			logging.debug(ret)
		except Exception as e:
			logging.error(e)
			return self.write({"errno":RET.DATAEXIST, "errmsg":"手机号已注册！"})
		self.write(dict(errno=RET.OK, errmsg="OK"))	


class LoginHandler(BaseHandler):
	""""""
	def post(self):
		mobile = self.json_args.get("mobile")
		passwd = self.json_args.get("password")
		# logging.debug(mobile)
		# logging.debug(passwd)
		if not all([mobile, passwd]):
			return self.write({"errno":RET.PARAMERR, "errmsg":"参数错误"})
		passwd = hashlib.sha256(config.passwd_hash_key+passwd).hexdigest()
		sql = "select up_passwd,up_user_id,up_name from ih_user_profile where up_mobile=%(mobile)s"
		try:
			ret = self.db.get(sql,mobile=mobile)
			# logging.debug(str(ret["up_passwd"]))
			# logging.debug(passwd)
		except Exception as e:
			logging.error(e)
			return 	self.write(dict(errno=RET.DBERR, errmsg="手机号或者密码有错误"))
		if ret and str(ret["up_passwd"]) == passwd:
			try:
				self.session = Session(self)
				self.session.data["mobile"] = mobile 
				self.session.data["user_id"] = ret["up_user_id"]
				self.session.data["name"] = ret["up_name"]
				self.session.save()		
			except Exception as e:
				logging.error(e)	 
			return self.write(dict(errno=RET.OK, errmsg="OK"))
		else:
			return self.write(dict(errno=RET.DATAERR,errmsg="手机号或者密码有错误"))
class CheckLoginHandler(BaseHandler):
	"""检查登陆状态"""
	def get(self):
		if self.get_current_user():
			return self.write({"errno":"0","errmsg":"已登陆","data":{"name":self.session.data.get("name")}})
		else:
			return self.write({"errno":"1","errmsg":"未登陆"})	

class LogOutHandler(BaseHandler):
	"""注销"""
	@require_logined
	def get(self):
		session_id = self.get_secure_cookie("session_id")
		try:
			self.redis.delete("sess_%s"%session_id)
		except Exception as e:
			logging.error(e)
			return self.write({"errno":"1", "errmsg":"False"})
		else:
			return self.write({"errno":"0", "errmsg":"True"})
		# try:
		# 	self.session.clear()
		# except Exception as e:
		# 	logging.error(e)
		# 	return self.write({"errno":"1", "errmsg":"False"})
		# else:
		# 	return self.write({"errno":"0", "errmsg":"True"})
				



		