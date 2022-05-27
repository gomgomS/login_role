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

class change_status_publish:    
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
        
        if data.get('change-status-to-editor') is not None:
            self.mgdDB.db_content_management.update_one(
                { "pkey"          : data['change-status-to-editor'] },
                { "$set"          : { "status_content"   : "inactive","status_publish"   : "editor" }} 
            ) 
            url = 'WRITE_CONTENT'
        elif data.get('change-status-to-redaction-approve') is not None:
            self.mgdDB.db_content_management.update_one(
                { "pkey"          : data['change-status-to-redaction-approve'] },
                { "$set"          : { "status_content"   : "inactive","status_publish"   : "redaction" }} 
            ) 
            url = 'EDITOR_PAGE'  
        elif data.get('change-status-to-redaction-reject') is not None:
            self.mgdDB.db_content_management.update_one(
                { "pkey"          : data['change-status-to-redaction-reject'] },
                { "$set"          : { "status_content"   : "rejected","status_publish"   : "jurnalist" }} 
            ) 
            url = 'EDITOR_PAGE'        
        elif data.get('change-status-reject-publish') is not None:
            self.mgdDB.db_content_management.update_one(
                { "pkey"          : data['change-status-reject-publish'] },
                { "$set"          : { "status_publish"   : "rejected" ,"status_content"   : "rejected" }} 
            ) 
            url = 'REDACTION_PAGE' 
        elif data.get('change-status-accept-publish') is not None:
            self.mgdDB.db_content_management.update_one(
                { "pkey"          : data['change-status-accept-publish'] },
                { "$set"          : { "status_content"   : "inactive", "status_publish"   : "accept" }} 
            ) 
            url = 'REDACTION_PAGE' 
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
# end class
