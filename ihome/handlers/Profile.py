#coding=utf-8

import logging
import re
from .BaseHandler import BaseHandler
from utils.common import require_logined
from utils.response_code import RET


class ProFileHandler(BaseHandler):
	"""获取用户个人信息"""
	@require_logined
	def get(self):
		try:
			name = self.session.data["name"]
			mobile = self.session.data["mobile"]
		except Exception as e:
			logging.error(e) 
			return 	self.write(dict(errno=RET.DBERR, errmsg="查询出错"))
		else:
			data = {
				"name":name,
				"mobile":mobile
			}
			return self.write(dict(errno=RET.OK, errmsg="OK", data=data))

class NameHandler(BaseHandler):
	""""""
	@require_logined
	def post(self):
		mobile = self.session.data["mobile"]
		name = self.json_args.get("name")
		sql1 = "select count(*) counts from ih_user_profile where up_name=%(name)s"
		sql = "update ih_user_profile set up_name=%(name)s where up_mobile =%(mobile)s"
		try:
			res = self.db.get(sql1,name=name)
			logging.debug(res["counts"])
		except Exception as e:
			logging.error(e) 
			return 	self.write(dict(errno=RET.DBERR, errmsg="查询出错"))
		if res["counts"]:
			return self.write(dict(errno=RET.DATAEXIST,errmsg="名字已经存在"))		
		try:
			ret = self.db.execute(sql,name=name,mobile=mobile)
			logging.debug(ret)
		except Exception as e:
			logging.error(e)
			return 	self.write(dict(errno=RET.DBERR, errmsg="数据库更新出错"))
		else:
			return self.write(dict(errno=RET.OK, errmsg="OK"))

class AuthHandler(BaseHandler):
	"""实名认证"""
	#接受数据存储
	@require_logined
	def post(self):
		mobile = self.session.data["mobile"]
		id_card = self.json_args.get("idcard")
		real_name = self.json_args.get("realname")
		# logging.debug(id_card)
		# logging.debug(real_name)
		if id_card.re.match(r"^(\d{15}$|^\d{18}$|^\d{17}(\d|X|x))$"):
			sql = "update ih_user_profile set up_real_name=%(real_name)s where up_mobile=%(mobile)s"
			try:
				self.db.execute(sql,real_name=real_name,mobile=mobile)
			except Exception as e:
				logging.error(e)
				return self.write(dict(errno=RET.DBERR, errmsg="数据更新出错"))
			else:
				return self.write(dict(errno=RET.OK, errmsg="OK"))	
		else:
	
			return self.write(dict(errno=RET.DATAERR,errmsg="数据填写错误"))
	#读取认证信息		
	@require_logined		
	def get(self):				
		pass




