#coding=utf-8
import logging
from functools import wraps
from utils.response_code import RET

def require_logined(fun):
	@wraps(fun)
	def wrapper(request_handler, *args, **kwargs):
		#根据get_current_user方法判断，如果返回来的不是空字典，说明用户已经登陆，redis中已经存储了session数据
		if request_handler.get_current_user():
			fun(request_handler, *args, **kwargs)
		else:
			#返回一个空字典说明用户没有登陆,redis中没有session数据
			request_handler.write(dict(errno=RET.SESSIONERR, errmsg="用户未登录"))
	return wrapper	