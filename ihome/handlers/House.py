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
        try:
            ret = self.redis.get("area_info")
        except Exception as e:
            logging.error(e)
            ret = None
        if ret:
           return self.write('{"errno":%s, "errmsg":"OK", "areas":%s}' %(RET.OK,ret))     
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
            self.redis.setex("area_info",constants.AREA_INFO_REDIS_EXPIRES_SECONDS, json.dumps(areas))
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

class NewHouseHandler(BaseHandler):
    """"""
    @require_logined
    def post(self):
        #获取参数
        '''
        {u'area_id': u'1', u'capacity': u'7', u'title': u'1', u'price': u'2', u'facility': [u'1'], u'acreage': u'5', u'beds': u'8', u'room_count': u'4', u'max_days': u'10', u'deposit': u'9', u'address': u'3', u'min_days': u'0', u'unit': u'6'}
        '''
        # logging.debug(self.json_args)
        user_id = self.session.data.get("user_id")
        title = self.json_args.get("title", "")
        price = self.json_args.get("price", "")
        acreage = self.json_args.get("acreage", "")
        area_id = self.json_args.get("area_id", "")
        capacity = self.json_args.get("capacity", "")
        beds = self.json_args.get("beds", "")
        room_count = self.json_args.get("room_count", "")
        max_days = self.json_args.get("max_days", "")
        deposit = self.json_args.get("deposit", "")
        address = self.json_args.get("address","")
        min_days = self.json_args.get("min_days", "")
        unit = self.json_args.get("unit", "")
        #校验
        if not all((title,price,acreage,area_id,capacity,beds,room_count,max_days,deposit,address,min_days,unit)):
            return self.write(dict(errno=RET.PARAMERR, errmsg="缺少参数"))
        try:
            price = int(price)*100
            deposit = int(deposit)*100
        except Exception as e:
            logging.error(e) 
            return self.write(dict(errno=RET.PARAMERR, errmsg="参数错误"))         
        try:
            sql = "insert into ih_house_info (hi_user_id, hi_title, hi_price, hi_acreage, hi_area_id, hi_capacity, hi_beds, hi_room_count, hi_max_days, hi_deposit, hi_address, hi_min_days, hi_house_unit) values(%(user_id)s,%(title)s,%(price)s,%(acreage)s,%(area_id)s,%(capacity)s,%(beds)s,%(room_count)s,%(max_days)s,%(deposit)s,%(address)s,%(min_days)s,%(unit)s)"
            house_id = self.db.execute(sql,user_id=user_id,title=title,price=price,acreage=acreage,area_id=area_id,capacity=capacity,beds=beds,room_count=room_count,max_days=max_days,deposit=deposit,address=address,min_days=min_days,unit=unit)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="插入数据库失败"))
        # logging.debug(house_id)
              

       

                  




