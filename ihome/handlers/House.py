#coding=utf-8

import logging
import constants
import json
import time
import config
from .BaseHandler import BaseHandler
from utils.response_code import RET
from utils.common import require_logined

class AreaInfoHandler(BaseHandler):
    """"""
    def get(self):
        # try:
        #     ret = self.redis.get("area_info")
        # except Exception as e:
        #     logging.error(e)
        #     ret = None
        # if ret:
        #    return self.write('{"errno":%s, "errmsg":"OK", "data":%s}' %(RET.OK,ret))     
        sql = "select ai_name,ai_area_id from ih_area_info"
        try:
            ret = self.db.query(sql)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="查询出错"))
        if not ret:
            return self.write(dict(errno=RET.NODATA, errmsg="no area data"))
        areas = []
        for l in ret:
            area = {
                "name":l["ai_name"],
                "area_id":l["ai_area_id"]
            }            
            areas.append(area)
        try:
            self.redis.setex("area_info",constants.AREA_INFO_REDIS_EXPIRES_SECONDS, areas)
        except Exception as e:
            logging.error(e)        
        self.write({"errno":"0", "errmsg":"OK","areas":areas})

class MyHouseHandler(BaseHandler):
    """"""
    @require_logined
    def get(self):
        user_id = self.session.data["user_id"]
        sql ="select a.hi_house_id,a.hi_title,a.hi_price,a.hi_ctime,a.hi_index_image_url,b.ai_name from ih_house_info a left join ih_area_info b on a.hi_area_id = b.ai_area_id where hi_user_id=%(user_id)s"
        try:
            res = self.db.query(sql,user_id=user_id)
        except Exception as e:
            logging.error(e)    
            return self.write(dict(errno=RET.DBERR, errmsg="查询出错"))
        houses = []    
        if res:
            for l in res:
                house = {
                    "house_id":l["hi_house_id"],
                    "title":l["hi_title"],
                    "price":l["hi_price"],
                    "ctime":l["hi_time"].time.strftime("%Y-%m-%d"),
                    "img_url":config.image_url_prefix + l["hi_index_image_url"] if l["hi_index_image_url"] else "",
                    "area_name":l["ai_name"]

                }
                houses.append(house) 
        try:
            ret = self.db.get("select up_real_name from ih_user_profile")
            logging.debug(ret)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="查询出错"))
        if ret["up_real_name"]:
            return self.write({"errno":"0", "errmsg":"have verified", "houses":houses})
        else:
            return self.write({"errno":"1", "errmsg":"have no verify"})




