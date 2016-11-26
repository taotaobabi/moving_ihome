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
		mobile = self.session.data["mobile"]
		sql = "select up_name from ih_user_profile where up_mobile=%(mobile)s"
		try:
			ret = self.db.get(sql,mobile=mobile)
		except Exception as e:
			logging.error(e) 
			return 	self.write(dict(errno=RET.DBERR, errmsg="查询出错"))
		else:
			self.session.data["name"] = ret["up_name"]
			name = self.session.data["name"]
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
		if re.match(r"^(\d{15}$|^\d{18}$|^\d{17}(\d|X|x))$", str(id_card)):
			sql = "update ih_user_profile set up_real_name=%(real_name)s,up_id_card=%(id_card)s where up_mobile=%(mobile)s"
			try:
				ret = self.db.execute_rowcount(sql,real_name=real_name,mobile=mobile,id_card=id_card)
				# logging.debug(ret)
			except Exception as e:
				logging.error(e)
			if not ret:	
				return self.write(dict(errno=RET.DBERR, errmsg="数据更新出错"))
			else:
				return self.write(dict(errno=RET.OK, errmsg="OK"))	
		else:
	
			return self.write(dict(errno=RET.DATAERR,errmsg="数据填写错误"))
	#读取认证信息		
	@require_logined		
	def get(self):				
		mobile = self.session.data["mobile"]
		sql = "select up_real_name,up_id_card from ih_user_profile where up_mobile=%(mobile)s"
		try:
			ret = self.db.get(sql,mobile=mobile)
			logging.debug(ret["up_real_name"])
		except Exception as e:
			logging.error(e) 
			return 	self.write(dict(errno=RET.DBERR, errmsg="查询出错"))
		else:
			if ret["up_real_name"] and ret["up_id_card"]:
				data = {
					"name":ret["up_real_name"],
					"idcard":ret["up_id_card"]
				}
				return self.write({"errno":"1", "errmsg":"用户已经实名认证过了", "data":data})
			else:
				
				return self.write({"errno":"0", "errmsg":"用户没有实名认证"})





