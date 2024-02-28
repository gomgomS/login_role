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

class view_content:
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
        data = params

        content = data.get('menu_value')

        ALL_DATA = []      

        if session.get('username') is None:
            launcher_content = 'login.html'   
            response = 'login'              
            return response        
        elif content == 'MANAGE_CONTENT':
            launcher_content = 'manage_content.html'
            manage_content_view     = self.mgdDB.db_content_management.find(
                {
                    "status": {"$not":{"$regex":"DEACTIVE"}},
                    "status_content": 'inactive'
                }
            )             
            ALL_DATA     = list( manage_content_view )
        elif content == 'LIST_LIVE_CONTENT':
            if session.get('role') == 'redaksi':
                launcher_content = 'list_live_content.html'
                manage_content_view     = self.mgdDB.db_content_management.find(
                    {
                        "status": {"$not":{"$regex":"DEACTIVE"}},
                        "status_content": 'live'
                    }
                )   
                ALL_DATA     = list( manage_content_view )
            else:
                return 'anda tidak memiliki akses'
        elif content == 'LIST_END_CONTENT':
            if session.get('role') == 'redaksi':
                launcher_content = 'list_end_content.html'            
                manage_content_view     = self.mgdDB.db_content_management.find(
                    {
                        "status": {"$not":{"$regex":"DEACTIVE"}},
                        "status_content": 'expired'
                    }
                ) 
                ALL_DATA     = list( manage_content_view )
            else:
                return 'anda tidak memiliki akses'
        elif content == 'WRITE_CONTENT':
            if session.get('role') == 'jurnalist':
                launcher_content = 'write_content.html'            
                manage_content_view_jurnalist     = self.mgdDB.db_content_management.find(
                    {
                        "status": {"$not":{"$regex":"DEACTIVE"}},
                        "status_publish": 'jurnalist'
                    }
                ) 
                ALL_DATA_JURNALIST    = list( manage_content_view_jurnalist )

                manage_content_view_editor    = self.mgdDB.db_content_management.find(
                    {
                        "status": {"$not":{"$regex":"DEACTIVE"}},
                        "status_publish": {"$not":{"$regex":"jurnalist"}},
                        # "status_publish": 'editor'
                    }
                ) 
                ALL_DATA_EDITOR     = list( manage_content_view_editor )

                response = render_template(
                    launcher_content,
                    ALL_DATA_JURNALIST = ALL_DATA_JURNALIST,
                    ALL_DATA_EDITOR    = ALL_DATA_EDITOR
                )

                return response
            else:
                return 'anda tidak memiliki akses'
        elif content == 'EDITOR_PAGE':
            if session.get('role') == 'editor':
                launcher_content = 'editor_page.html'  
                manage_content_view_editor   = self.mgdDB.db_content_management.find(
                    {
                        "status": {"$not":{"$regex":"DEACTIVE"}},
                        "$and"     : [{"status_publish": 'editor'},
                            {"status_content" :{"$not":{"$regex":'redaction'}}},
                            {"status_content" :{"$not":{"$regex":'rejected'}}},]
                    }
                ) 
                ALL_DATA_JURNALIST  = list( manage_content_view_editor)
            
                manage_content_view_accept    = self.mgdDB.db_content_management.find(
                    {
                        "status": {"$not":{"$regex":"DEACTIVE"}},
                        "status_publish": 'redaction'
                    }
                ) 
                ALL_DATA_JURNALIST_ACCEPT  = list( manage_content_view_accept )

                manage_content_view_rejected    = self.mgdDB.db_content_management.find(
                    {
                        "status": {"$not":{"$regex":"DEACTIVE"}},
                        "status_publish": 'jurnalist',
                        "status_content": 'rejected'
                    }
                ) 
                ALL_DATA_JURNALIST_REJECTED     = list( manage_content_view_rejected )

                response = render_template(
                    launcher_content,
                    ALL_DATA_JURNALIST = ALL_DATA_JURNALIST,                
                    ALL_DATA_JURNALIST_ACCEPT = ALL_DATA_JURNALIST_ACCEPT,
                    ALL_DATA_JURNALIST_REJECTED   = ALL_DATA_JURNALIST_REJECTED
                )

                return response
            else:
                return 'anda tidak memiliki akses'
        elif content == 'REDACTION_PAGE':
            if session.get('role') == 'redaksi':
                launcher_content = 'redaction_page.html'  
                manage_content_view_editor   = self.mgdDB.db_content_management.find(
                    {
                        "status": {"$not":{"$regex":"DEACTIVE"}},
                        "$and"     : [{"status_publish": 'redaction'},                        
                            {"status_content" :{"$not":{"$regex":'rejected'}}}]
                    }
                ) 
                ALL_DATA_EDITOR  = list( manage_content_view_editor)            
            
                manage_content_view_accept    = self.mgdDB.db_content_management.find(
                    {
                        "status": {"$not":{"$regex":"DEACTIVE"}},
                        "status_publish": 'accept',
                    }
                ) 
                ALL_DATA_EDITOR_ACCEPT  = list( manage_content_view_accept )

                manage_content_view_rejected    = self.mgdDB.db_content_management.find(
                    {
                        "status": {"$not":{"$regex":"DEACTIVE"}},
                        "status_publish": 'rejected',
                        "status_content": 'rejected'
                    }
                ) 
                ALL_DATA_EDITOR_REJECTED     = list( manage_content_view_rejected )

                response = render_template(
                    launcher_content,
                    ALL_DATA_EDITOR = ALL_DATA_EDITOR,                
                    ALL_DATA_EDITOR_ACCEPT = ALL_DATA_EDITOR_ACCEPT,
                    ALL_DATA_EDITOR_REJECTED   = ALL_DATA_EDITOR_REJECTED
                )

                return response     
            else:
                return 'anda tidak memiliki akses'   
        else:
            # launcher_content = 'view_content.html'
            # ALL_DATA = session.get('role')
            return 'halaman tidak ditemukan'
        
        response = render_template(
            launcher_content,
            ALL_DATA = ALL_DATA
        )

        return response
    # end def
# end class
