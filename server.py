import json
import time
import pymongo
import sys
import urllib.parse
import base64

sys.path.append("pytavia_core"    ) 
sys.path.append("pytavia_settings") 
sys.path.append("pytavia_stdlib"  ) 
sys.path.append("pytavia_storage" ) 
sys.path.append("pytavia_modules" ) 
sys.path.append("pytavia_modules/rest_api_controller")
sys.path.append("pytavia_modules/management_content") 

# from datetime          import datetime

# from apscheduler.schedulers.background import BackgroundScheduler


# adding comments
from pytavia_stdlib  import utils
from pytavia_core    import database 
from pytavia_core    import config 
from pytavia_core    import model
from pytavia_stdlib  import idgen 

from rest_api_controller import module1 

from management_content import view_content
from management_content import save_content
from management_content import delete_content
from management_content import change_status_live_content
from management_content import news

from management_content import edit_write_content
from management_content import update_write_content
from management_content import save_content_process
from management_content import change_status_publish

from management_content import nav_view_app

from auth import register_view_app
from auth import login_view_app
from auth import register_app
from auth import login_app

##########################################################

from flask import request
from flask import render_template
from flask import Flask
from flask import session
from flask import make_response
from flask import redirect
from flask import url_for
from flask import flash


from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import CSRFError
#
# Main app configurations
#
app             = Flask( __name__, config.G_STATIC_URL_PATH )
# csrf            = CSRFProtect(app)
app.secret_key  = config.G_FLASK_SECRET
app.db_update_context, app.db_table_fks = model.get_db_table_paths(model.db)

# sched = BackgroundScheduler()    

########################## CALLBACK API ###################################

@app.route("/hi", methods=["GET"])
def api_hi():
    return 'check conn!!'
# end def

@app.route("/nav", methods=["GET"])
def nav_view():  
    params = request.args.to_dict()    
    response = nav_view_app.nav_view_app(app).process( params )    
    return response
# end def

@app.route("/login/<info_error>", methods=["GET"])
def login_view_direct(info_error):          
    params = {**request.args.to_dict(), **info_error}
    response = login_view_app.login_view_app(app).process( params )
    return response
# end def

@app.route("/login", methods=["GET"])
def login_view():  
    params = request.args.to_dict()    
    response = login_view_app.login_view_app(app).process( params )    
    return response
# end def

@app.route("/register", methods=["GET"])
def register_view():  
    params = request.args.to_dict()    
    response = register_view_app.register_view_app(app).process( params )
    return response
# end def

@app.route("/login_app", methods=["POST"])
def login_to_apps():  
    params = request.args.to_dict()    
    response = login_app.login_app(app).process( params )

    # check if respnse is list or not    
    res = list(response.keys())[0]   
    if res == "menu_value":             
        return redirect(url_for('content_direct',menu_value=response[res]))             
    return login_view_direct(info_error=response)
# end def

@app.route("/register_app", methods=["POST"])
def register_to_apps():  
    params = request.args.to_dict()    
    response = register_app.register_app(app).process( params )
    return response
# end def

@app.route("/logout", methods=["POST","GET"])
def logout():  
    session.clear()
    return  redirect(url_for('login_view'))  
# end def

@app.route("/news", methods=["GET"])
def launch_news():  
    params = request.args.to_dict()    
    response = news.news(app).process( params )
    return response
# end def

@app.route("/launcher", methods=["GET"])
def content():  
    params = request.args.to_dict()    
    response = view_content.view_content(app).process( params )
    if response == 'login':
        return redirect(url_for('login_view'))  
    return response
# end def

@app.route("/launcher", methods=["GET"])
def content_direct(menu_value):  
    params = request.args.to_dict()    
    response = view_content.view_content(app).process( params )
    if response == 'login':
        return redirect(url_for('login_view'))  
    return response
# end def

@app.route("/save_content", methods=["POST"])
def save_content_data():
    params = request.args.to_dict()    
    response = save_content.save_content(app).process( params )           
    # temporari
    # sched.add_job(temp, run_date='2022-05-22 20:35:00')
    # sched.start()
    # end temp

    res = list(response.keys())[0]        
    return redirect(url_for('content_direct',menu_value=response[res]))  
    return response
# end def

@app.route("/save_content_process", methods=["POST"])
def save_content_process_data():
    params = request.args.to_dict()    
    response = save_content_process.save_content_process(app).process( params )        
    res = list(response.keys())[0]        
    return redirect(url_for('content_direct',menu_value=response[res]))  
    return response
# end def

@app.route("/delete", methods=["POST"])
def delete_content_data():  
    params = request.args.to_dict()    
    response = delete_content.delete_content(app).process( params )    
    res = list(response.keys())[0]  #take first key in list     
    return redirect(url_for('content_direct',menu_value=response[res]))      
# end def

@app.route("/change-status-live-content", methods=["POST"])
def change_status_live_content_data():  
    params = request.args.to_dict()    
    response = change_status_live_content.change_status_live_content(app).process( params )      
    res = list(response.keys())[0]  #take first key in list     
    return redirect(url_for('content_direct',menu_value=response[res]))      
# end def

@app.route("/change-status-publish", methods=["POST"])
def change_status_publish_data():  
    params = request.args.to_dict()    
    response = change_status_publish.change_status_publish(app).process( params )            
    res = list(response.keys())[0]  #take first key in list     
    return redirect(url_for('content_direct',menu_value=response[res]))      
# end def

@app.route("/writecontent/edit/<pkey>", methods=["GET"])
def edit_write_content_data(pkey):    
    params = request.args.to_dict()    
    params['pkey'] = pkey    
    response = edit_write_content.edit_write_content(app).process( params )  
    return response     
    res = list(response.keys())[0]        
    return redirect(url_for('content_direct',menu_value=response[res]))  
    return response
# end def

@app.route("/writecontent/update", methods=["POST"])
def update_write_content_data():    
    params = request.args.to_dict()          
    response = update_write_content.update_write_content(app).process( params )         
    res = list(response.keys())[0]        
    return redirect(url_for('content_direct',menu_value=response[res]))  
    return response
# end def

# def temp():
#     mgdDB = database.get_db_conn(config.mainDB)
#     mgdDB.db_content_management.update_one(
#             { "pkey"          : '628a16f19499ba4469b9e5a1-faa8dcb21783d03d1493408be110490688c62e4f5cfc8e9f-8692663' },
#             { "$set"          : { "content"   : "astffff DEACTIVE INI" }} 
#         )

# @app.route("/updateschedule", methods=["POST"])
# def updateform():
#     params = request.args.to_dict()
#     response = update_schedule_app.update_schedule_app(app).process( params )
#     return response
# # end def

@app.route("/v1/api/api-v1", methods=["GET"])
def api_v1():
    params = request.args.to_dict()
    response = module1.module1(app).process( params )
    return response.stringify_v1()
# end def

@app.route("/v1/api/api-post-v1", methods=["POST"])
def api_post_v1():
    params = request.form.to_dict()
    response = module1.module1(app).process( params )
    return response.stringify_v1()
# end def

### Sample generic endpoints
"""
# TODO: update example using new db actions
### sample generic archive -- archive book
@app.route("/process/book/archive", methods=["POST"])
def book_proc_archive():
    params = request.form.to_dict()
    response = generic_proc.generic_proc(app).archive({
        "collection"    : "db_book",
        "pkey"          : params["pkey"]
    })

    if response.get('status_code') == config.G_STATUS['SUCCESS']['CODE']:
        return response.http_stringify()
    else:
        return response.http_stringify()

### sample generic restore -- restore book
@app.route("/process/book/restore", methods=["POST"])
def book_proc_restore():
    params = request.form.to_dict()
    response = generic_proc.generic_proc(app).restore({
        "collection"    : "db_book",
        "pkey"          : params["pkey"]
    })

    if response.get('status_code') == config.G_STATUS['SUCCESS']['CODE']:
        return response.http_stringify()
    else:
        return response.http_stringify()

### sample two way reference -- reference book to author and author to book
@app.route("/process/book/add_author", methods=["POST"])
def book_proc_add_author():
    params = request.form.to_dict()
    response = generic_proc.generic_proc(app).add_two_way_reference({
        "main"  : {
            "collection"    : "db_book",
            "pkey"          : params["book_pkey"]
        },  
        "sub"  : {
            "collection"    : "db_author",
            "pkey"          : params["author_pkey"]
        }
    })

    if response.get('status_code') == config.G_STATUS['SUCCESS']['CODE']:
        return response.http_stringify()
    else:
        return response.http_stringify()

### sample remove two way reference -- dereference book to author and vise versa
@app.route("/process/book/remove_group", methods=["POST"])
def book_proc_remove_group():
    params = request.form.to_dict()
    response = generic_proc.generic_proc(app).remove_two_way_reference({
        "main"  : {
            "collection"    : "db_book",
            "pkey"          : params["book_pkey"]
        },  
        "sub"  : {
            "collection"    : "db_author",
            "pkey"          : params["author_pkey"]
        }
    })

    if response.get('status_code') == config.G_STATUS['SUCCESS']['CODE']:
        return response.http_stringify()
    else:
        return response.http_stringify()
"""