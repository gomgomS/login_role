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
from flask             import session

from pytavia_stdlib    import idgen
from pytavia_stdlib    import utils
from pytavia_core      import database
from pytavia_core      import config
from pytavia_core      import helper
from pytavia_core      import bulk_db_insert
from pytavia_core      import bulk_db_update
from pytavia_core      import bulk_db_multi

from datetime          import datetime

from apscheduler.schedulers.background import BackgroundScheduler

class update_write_content:    
    mgdDB = database.get_db_conn(config.mainDB)      

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

        title             = data["title"]
        content           = data["content"]
        start_date        = data["start_date"]
        end_date          = data["end_date"]      
        status_content    = 'inactive'          
        status_publish    = 'jurnalist'  

        self.mgdDB.db_content_management.update_one(
                { "pkey"          : data['pkey'] },
                { "$set"          : {"title"   : title,
                                    "content" : content,
                                    "start_date" : start_date,
                                    "end_date" : end_date}             
                } 
            ) 
                
        if  session.get('role') == 'jurnalist':
            role_page = 'WRITE_CONTENT'
        elif session.get('role') == 'editor':
            role_page = 'EDITOR_PAGE'
        else:
            role_page = 'REDACTION_PAGE'
            
        response = {
            'menu_value' : role_page            
        } 
        
        return response    
    # end def
    
# end class
