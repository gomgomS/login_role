import json
import time
import pymongo
import sys
import urllib.parse
import base64
import traceback
import random
import urllib.request
import io
import requests
import json
import hashlib

sys.path.append("pytavia_core")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")
sys.path.append("pytavia_modules")
sys.path.append("pytavia_modules")


from flask             import render_template_string
from flask             import render_template
from flask             import request

from pytavia_stdlib    import idgen
from pytavia_stdlib    import utils
from pytavia_core      import database
from pytavia_core      import config
from pytavia_core      import helper
from pytavia_core      import bulk_db_insert
from pytavia_core      import bulk_db_update
from pytavia_core      import bulk_db_multi

from apscheduler.schedulers.background import BackgroundScheduler

class change_status_live_content:    
    mgdDB = database.get_db_conn(config.mainDB)       
    sched = BackgroundScheduler()    
    sched.start()      

    def __init__(self, app):
        self.webapp = app        
    # end def

    def process(self, params):        
        response = helper.response_msg(
            "CREATE_COMPANY_SUCCESS",
            "CREATE COMPANY SUCCESS", {},
            "0000"
        )
        
        data = request.form        
        if str(data.get('change-status-expired')) != 'None':
            self.mgdDB.db_content_management.update_one(
                { "pkey"          : data['change-status-expired'] },
                { "$set"          : { "status_content"   : "expired" }} 
            ) 
            url = 'LIST_LIVE_CONTENT'
        if data.get('change-status-start-schedule') is not None:
            self.mgdDB.db_content_management.update_one(
                { "pkey"          : data['change-status-start-schedule'] },
                { "$set"          : { "status_content"   : "inactive" }} 
            ) 

            get_data_content   = self.mgdDB.db_content_management.find_one(
                {
                    "pkey"          : data['change-status-start-schedule']
                }
            )
            
            # start start-date cronjob
            y = self.loop_scheduler_start(get_data_content['pkey'],get_data_content['start_date'])  
            # end end-date cronjob   
            # start start-date cronjob
            y = self.loop_scheduler_end(get_data_content['pkey'],get_data_content['end_date'])  
            # end end-date cronjob
            url = 'LIST_LIVE_CONTENT'
        else:    
            self.mgdDB.db_content_management.update_one(
                { "pkey"          : data['change-status'] },
                { "$set"          : { "status_content"   : "live" }} 
            ) 
            url = 'MANAGE_CONTENT'
        
        response = {
            'menu_value' : url
        }

        return response
    # end def    

    def loop_scheduler_start(self,pkey,start_date):        
        x = self.sched.add_job(self.temp_scheduler,'date', run_date=start_date, args=[{'pkey':pkey,'status_content':'live'}], replace_existing=True)        
    # end def

    def loop_scheduler_end(self,pkey,end_date):        
        x = self.sched.add_job(self.temp_scheduler,'date', run_date=end_date, args=[{'pkey':pkey,'status_content':'expired'}], replace_existing=True)        
    # end def

    def temp_scheduler(self,args):          
        self.mgdDB.db_content_management.update_one(
            { "pkey"          : args['pkey']},
            { "$set"          : { "status_content"   : args['status_content'] }} 
        )
    # end def

# end class
