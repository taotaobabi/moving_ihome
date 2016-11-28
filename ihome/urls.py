#coding=utf-8

import os

from handlers import Passport, VerifyCode, Profile, House
from handlers.BaseHandler import StaticFileHandler

handlers = [
	(r'^/api/house/new$',House.NewHouseHandler),
	(r'^/api/house/my$',House.MyHouseHandler),
	(r'^/api/house/area$',House.AreaInfoHandler),
	(r'^/api/profile/avatar$',Profile.AvatarHandler),
	(r'^/api/profile/auth$',Profile.AuthHandler),
	(r'^/api/profile/name$',Profile.NameHandler),
	(r'^/api/profile$',Profile.ProFileHandler),
	(r'^/api/logout$',Passport.LogOutHandler),
	(r'^/api/checklogin$',Passport.CheckLoginHandler),
	(r'^/api/login$',Passport.LoginHandler),
	(r'^/api/register$',Passport.RegisterHandler),
	(r"^/api/smscode$",VerifyCode.SMSCodeHandler),
	(r"^/api/imagecode$", VerifyCode.ImageCodeHandler),
	(r"/(.*)",StaticFileHandler,dict(path=os.path.join(os.path.dirname(__file__),"html"),default_filename="index.html"))

]
