
#################################################################################
#
# {___     {__          {__       {__
# {_ {__   {__          {_ {__   {___
# {__ {__  {__   {__    {__ {__ { {__
# {__  {__ {__ {__  {__ {__  {__  {__
# {__   {_ {__{__    {__{__   {_  {__
# {__    {_ __ {__  {__ {__       {__
# {__      {__   {__    {__       {__
#
# (C) Copyright European Space Agency, 2024
# 
# This file is subject to the terms and conditions defined in file 'LICENCE.txt', 
# which is part of this source code package. No part of the package, including 
# this file, may be copied, modified, propagated, or distributed except 
# according to the terms contained in the file ‘LICENCE.txt’.“ 
#
#################################################################################

import os
import time
import json
import html
import random
from datetime import datetime
from importlib.metadata import version
from flask import Blueprint , render_template , request , g as _g , redirect , url_for , make_response
from werkzeug.utils import secure_filename
from esanom import database as _database , util as _util , config as _config
from . import common as _common 

#####################################################################

ROUTES = Blueprint( "routes" , __name__ , template_folder = "templates" , static_folder='static' )

#####################################################################

@ROUTES.before_request
def before_request_func( ) :
    _g._benchmark_before_request = time.time( )

@ROUTES.after_request
def after_request_func( resp ) :

#    resp.cache_control.max_age = 600

#    resp.cache_control.no_cache = True
#    resp.cache_control.no_store = True
    #resp.cache_control.must_revalidate = False
    #resp.cache_control.proxy_revalidate = False

    if "text/html" not in resp.headers[ "Content-Type" ] : return( resp )

    cookie_key = request.cookies.get( "key" , "" )
    #if cookie_key.strip( ) != "" : return( resp )
    if len( cookie_key ) == 64 : return( resp )

    ####

    session_key = _util.generate_rhash( )
    resp.set_cookie( "key" , session_key , secure = True , samesite = "Strict" )

    ####

    return( resp )

@ROUTES.app_template_filter( "filter_self_basename" )
def filter_self_basename( s ):
    # <TemplateReference 'pages/account/inc_admin_nav.html'>
    parts = str( s ).split( "'" )
    if len( parts ) != 3 : return( None )
    return( os.path.basename( parts[ 1 ] ).removesuffix( ".html" ) )

#####################################################################

@ROUTES.route( "/error_404" , methods = [ "GET" ] )
def page_error_404( ) :
    return( render_template( "error_404.html" ) , 404 )

@ROUTES.route( "/error_500" , methods = [ "GET" ] )
def page_error_500( ) :
    return( render_template( "error_500.html" ) , 500 )

#####################################################################

@ROUTES.app_context_processor
def app_context_processor( ) :

    session_data = { }
    session_key = request.cookies.get( "key" , "" ).strip( )
    if len( session_key ) == 64 :
        session_row = _database.db_query_select_row( "SELECT * from `session` WHERE `key`=%s LIMIT 1" , [ session_key ] )
        if session_row != None :
            session_data = json.loads( session_row[ "data" ] ) 



    # FIXME TODO should be optimized
    system_databaseversion_row = _database.db_query_select_row( "SELECT * from `system` WHERE `key`=%s LIMIT 1" , [ "database/version" ] )
    system_orchestratortime_row = _database.db_query_select_row( "SELECT * from `system` WHERE `key`=%s LIMIT 1" , [ "orchestrator/time" ] )
    system_schedulertime_row = _database.db_query_select_row( "SELECT * from `system` WHERE `key`=%s LIMIT 1" , [ "scheduler/time" ] )

    orchestrator_time_dt = round( time.time( ) - system_orchestratortime_row[ "val_int" ] )
    scheduler_time_dt = round( time.time( ) - system_schedulertime_row[ "val_int" ] )

    ####

    api_row = _database.db_query_select_row( "SELECT * from `api` WHERE `name` LIKE '%0_USER' LIMIT 1" )

    flag_sampledata = False 
    if api_row != None : flag_sampledata = True

    ####

    is_admin = False
    is_loggedin = False
    account_name = ""
    if session_data.get( "account_row" ) :
        is_loggedin = True
        account_name = session_data["account_row"]["name"]
        is_admin = ( account_name == "_admin" )

    is_fs_tmp = False
    if _config.DATA["fs_storage_path"].startswith("/tmp/"): is_fs_tmp = True

    data = {
        "config_data" : _config.DATA ,
        "admin_account_email" : "".join(f"&#{ord(c)};" for c in _config.DATA[ "admin_account_email" ] ) ,
        "nom_version" : version( "esanom" ) ,
        "database_version" : system_databaseversion_row[ "val_str" ] ,
        "orchestrator_time_dt" : orchestrator_time_dt ,
        "scheduler_time_dt" : scheduler_time_dt ,
        "year" : datetime.now( ).strftime( "%Y" ) ,
        "flag_sampledata" : flag_sampledata ,
        "benchmark" : round( time.time( ) - _g._benchmark_before_request , 3 ) ,
        "session_data" : session_data ,
        "is_loggedin" : is_loggedin ,
        "is_admin" : is_admin ,
        "account_name" : account_name ,
        "is_fs_tmp" : is_fs_tmp 
    }

    #print(data)

    return( dict( _tdata = data ) )

@ROUTES.app_template_global( "test" )
def app_template_global_test( n ) :
    return( f"{n}." )

#####################################################################

@ROUTES.route( "/" , methods = [ "GET" ] )
def page_index( ) :

    return( render_template( "page_index.html" ) )

@ROUTES.route( "/models" , methods = [ "GET" ] )
def page_models( ) :

    rolemodel_rows = _database.db_query_select_rows( "SELECT * from `rolemodel` where enable=1" )

    for rolemodel_row in rolemodel_rows :
        if rolemodel_row[ "heartbeat_at" ] != None :

            seconds = round( time.time( ) - rolemodel_row[ "heartbeat_at" ].timestamp( ) )

            mm, ss = divmod(seconds, 60)
            hh, mm = divmod(mm, 60)

            heartbeat_last_str = f"{hh}h {mm}m {ss}s"

            rolemodel_row[ "[heartbeat_last_str]" ] = f"{hh}h {mm}m {ss}s"
            rolemodel_row[ "[heartbeat_last]" ] = seconds

        else :
            rolemodel_row[ "[heartbeat_last]" ] = 99999

    columns = [ "uid" , "name" , "category" , "description" , "[heartbeat_last]" ]

    tdata = {
        "rows" : rolemodel_rows ,
        "columns" : columns
    }

    return( render_template( "pages/models/rows.html" , tdata = tdata ) )




@ROUTES.route( "/models_read" , methods = [ "GET" ] )
def page_models_read( ) :

    rolemodel_uid = _common.request_arg_str( "uid" )

    rolemodel_row = _database.db_query_select_row( "SELECT * from `rolemodel` WHERE uid=%s LIMIT 1" , [ rolemodel_uid ] )

    if rolemodel_row == None : return( render_template( "error_500.html" ) )

    ####

    mport_rows = _database.db_query_select_rows( "SELECT id,port_id,direction,enable,cardinal from mport where rolemodel_id=%s order by id" , [ rolemodel_row[ "id" ] ] )

    ####

    has_inputs = False
    has_outputs = False

    mpins = [ ]

    for mport_row in mport_rows :

        if mport_row["direction"] == "inputs" : has_inputs = True 
        if mport_row["direction"] == "outputs" : has_outputs = True 
        
        port_row = _database.db_query_select_row( "SELECT * from port where id=%s LIMIT 1" , [ mport_row[ "port_id" ] ] )

        mport_row[ "[port_name]"] = port_row[ "name" ]
        mport_row[ "[port_uid]"] = port_row[ "uid" ]

        mpin_rows = _database.db_query_select_rows( "SELECT id,mport_id,unit_id from mpin where mport_id=%s order by id" , [ mport_row["id"] ] )


        for mpin_row in mpin_rows :
            unit_row = _database.db_query_select_row( "SELECT * from unit where id=%s LIMIT 1" , [ mpin_row["unit_id"]] )
            pin_row = _database.db_query_select_row( "SELECT * from pin where id=%s LIMIT 1" , [ unit_row["pin_id"]] )
            port_pin_row = _database.db_query_select_row( "SELECT * from port_pin where port_id=%s and pin_id=%s LIMIT 1" , [port_row[ "id" ] , pin_row[ "id" ] ] )
            mpin_row[ "cardinal" ] = port_pin_row[ "cardinal" ]
            mpin_row[ "id" ] = pin_row[ "id" ]
            mpin_row[ "name" ] = pin_row[ "name" ]
            mpin_row[ "type" ] = pin_row[ "type" ]
            mpin_row[ "unit_name" ] = unit_row[ "name" ]
            mpin_row[ "port_name/pin_name(unit_name)" ] = port_row[ "name" ] + "/" + pin_row[ "name" ] + "(" + unit_row[ "name" ] + ")"


        mpins.append( mpin_rows )

        mport_row[ "[mpin_rows]" ] = mpin_rows


    mpin_columns = [ "name" , "cardinal" , "type" , "unit_name" ]

    tdata = {
        "row" : rolemodel_row ,
        "mport_rows" : mport_rows ,
        "has_inputs" : has_inputs ,
        "has_outputs" : has_outputs ,
        "mpin_columns" : mpin_columns
    }

    return( render_template( "pages/models/read.html" , tdata = tdata ) )



@ROUTES.route( "/ports" , methods = [ "GET" ] )
def page_ports( ) :


    rows = _database.db_query_select_rows( "SELECT * from `port`" )

    columns = [ "uid" , "name" , "description" ]

    tdata = {
        "rows" : rows ,
        "columns" : columns
    }

    return( render_template( "pages/ports/rows.html" , tdata = tdata ) )



@ROUTES.route( "/ports_read" , methods = [ "GET" ] )
def page_ports_read( ) :

    uid = _common.request_arg_str( "uid" )

    row = _database.db_query_select_row( "SELECT * from `port` WHERE uid=%s LIMIT 1" , [ uid ] )
    if row == None : return( render_template( "error_500.html" ) )

    port_pin_rows = _database.db_query_select_rows( "SELECT * from `port_pin` WHERE port_id=%s" , [ row["id"]] )

    for port_pin_row in port_pin_rows :
        pin_row = _database.db_query_select_row( "SELECT * from `pin` WHERE id=%s LIMIT 1" , [ port_pin_row["pin_id"]] )
        port_pin_row["[pin_name]"]=pin_row["name"]
        port_pin_row["[pin_type]"]=pin_row["type"]

    columns = ["[pin_name]","[pin_type]","cardinal"]

    ####


    tdata = {
        "row" : row ,
        "rows" : port_pin_rows,
        "columns" : columns
    }

    return( render_template( "pages/ports/read.html" , tdata = tdata ) )


####

@ROUTES.route( "/pins" , methods = [ "GET" ] )
def page_pins( ) :


    rows = _database.db_query_select_rows( "SELECT * from `pin`" )

    columns = [ "uid" , "name" , "type" , "description" ]

    tdata = {
        "rows" : rows ,
        "columns" : columns
    }

    return( render_template( "pages/pins/rows.html" , tdata = tdata ) )



@ROUTES.route( "/pins_read" , methods = [ "GET" ] )
def page_pins_read( ) :

    uid = _common.request_arg_str( "uid" )

    row = _database.db_query_select_row( "SELECT * from `pin` WHERE uid=%s LIMIT 1" , [ uid ] )
    if row == None : return( render_template( "error_500.html" ) )


    unit_rows = _database.db_query_select_rows( "SELECT * from `unit` WHERE pin_id=%s" , [ row["id"]] )

    unit_columns = ["name","description","symbol","default"]

    ####

    tdata = {
        "row" : row ,
        "unit_rows" : unit_rows,
        "unit_columns" : unit_columns
    }

    return( render_template( "pages/pins/read.html" , tdata = tdata ) )


@ROUTES.route( "/member_apis_read" , methods = [ "GET" ] )
def page_member_apis_read( ) :

    uid = _common.request_arg_str( "uid" )

    row = _database.db_query_select_row( "SELECT * from `api` WHERE uid=%s LIMIT 1" , [ uid ] )
    if row == None : return( render_template( "error_500.html" ) )

    ####

    tdata = {
        "row" : row 
    }

    return( render_template( "pages/member_apis/read.html" , tdata = tdata ) )



@ROUTES.route( "/member_apis_update" , methods = [ "GET" ] )
@_common.decorator_web_login_required( )
def page_member_apis_update( ) :

    uid = _common.request_arg_str( "uid" )

    row = _database.db_query_select_row( "SELECT * from `api` WHERE uid=%s LIMIT 1" , [ uid ] )
    if row is None : raise Exception( f"row None" )

    tdata = {
        "k1" : time.time( ) ,
        "row" : row 
    }

    #print(tdata)

    return( render_template( "pages/member_apis/update.html" , tdata = tdata ) )


@ROUTES.route( "/hx_member_apis_update" , methods = [ "POST" ] )
@_common.decorator_web_login_required( )
def hx_member_apis_update( ) :

    uid = _common.request_arg_str( "uid" )

    # FIXME TODO check if id is available and allowed
    #row = _database.db_query_select_row( "SELECT * from `group` WHERE id=%s LIMIT 1" , [id])
    #if row is None : raise Exception( f"row None" )

    ####

    form = request.form.to_dict( flat = False )
    print(form)

    ####
    row_data = { }

    for i , ( k , v ) in enumerate( form.items( ) ) :
        if k.startswith("[") : continue
        row_data[k]=v[0]


    is_new_token=False
    if "[new_token]" in form : 
        row_data["token"]=""
        is_new_token=True
        print("NEW TOKEN")

    #print(row_data)

    _database.update_fromdict( "api" , uid , row_data , cid = "uid" )
    ####

    row = _database.db_query_select_row( "SELECT * from `api` WHERE uid=%s LIMIT 1" , [ uid ] )
    if row is None : raise Exception( f"row None" )

    tdata = {
        "k1" : time.time( ) ,
        "row" : row,
        "is_new_token" : is_new_token
    }

    #print(tdata)

    response = make_response( render_template( "pages/member_apis/hx_form.html" , tdata = tdata ) )

    if not is_new_token :
        response.headers[ "HX-Redirect" ] = url_for( ".page_member_apis_read" , uid = uid )

    ####

    return( response )

####

@ROUTES.route( "/admin_accounts_read" , methods = [ "GET" ] )
def page_admin_accounts_read( ) :

    uid = _common.request_arg_str( "uid" )

    row = _database.db_query_select_row( "SELECT * from `account` WHERE uid=%s LIMIT 1" , [ uid ] )
    if row == None : return( render_template( "error_500.html" ) )

    ####

    tdata = {
        "row" : row 
    }

    return( render_template( "pages/admin_accounts/read.html" , tdata = tdata ) )


@ROUTES.route( "/admin_accounts_update" , methods = [ "GET" ] )
@_common.decorator_web_login_required( )
def page_admin_accounts_update( ) :

    uid = _common.request_arg_str( "uid" )

    row = _database.db_query_select_row( "SELECT * from `account` WHERE uid=%s LIMIT 1" , [ uid ] )
    if row is None : raise Exception( f"row None" )

    tdata = {
        "k1" : time.time( ) ,
        "row" : row 
    }

    #print(tdata)

    return( render_template( "pages/admin_accounts/update.html" , tdata = tdata ) )


@ROUTES.route( "/hx_admin_accounts_update" , methods = [ "POST" ] )
@_common.decorator_web_login_required( )
def hx_admin_accounts_update( ) :

    uid = _common.request_arg_str( "uid" )

    # FIXME TODO check if id is available and allowed
    #row = _database.db_query_select_row( "SELECT * from `group` WHERE id=%s LIMIT 1" , [id])
    #if row is None : raise Exception( f"row None" )

    ####

    form = request.form.to_dict( flat = False )
    print(form)

    ####
    row_data = { }

    for i , ( k , v ) in enumerate( form.items( ) ) :
        if k.startswith("[") : continue
        row_data[k]=v[0]


    if "[enable]" in form : 
        row_data[ "enable" ] = 1
    else :
        row_data[ "enable" ] = 0


    if "[email_confirmed]" in form : 
        row_data[ "email_confirmed" ] = 1
    else :
        row_data[ "email_confirmed" ] = 0


    if form["[password]"][0]!="" : 
        row_data[ "password" ] = form["[password]"][0]

    #print(row_data)

    _database.update_fromdict( "account" , uid , row_data , cid = "uid" )
    ####

    row = _database.db_query_select_row( "SELECT * from `account` WHERE uid=%s LIMIT 1" , [ uid ] )
    if row is None : raise Exception( f"row None" )

    tdata = {
        "k1" : time.time( ) ,
        "row" : row
    }

    #print(tdata)

    response = make_response( render_template( "pages/admin_accounts/hx_form.html" , tdata = tdata ) )

    response.headers[ "HX-Redirect" ] = url_for( ".page_admin_accounts_read" , uid = uid )

    ####

    return( response )


####

@ROUTES.route( "/docs" , methods = [ "GET" ] )
def page_docs( ) :
    return( render_template( "page_docs.html" ) )


@ROUTES.route( "/login" , methods = [ "GET" ] )
def page_login( ) :
    return( render_template( "pages/login/main.html" ) )

@ROUTES.route( "/logout" , methods = [ "GET" ] )
def page_logout( ) :
    session_key = request.cookies.get( "key" , "" ).strip( )
    if len( session_key ) == 64 :
        _database.db_query_delete( "DELETE FROM session WHERE `key`=%s LIMIT 1" , [ session_key ] )
    return( render_template( "pages/logout/main.html" ) )

@ROUTES.route( "/register" , methods = [ "GET" ] )
def page_register( ) :

    system_row = _database.db_query_select_row( "SELECT * from `system` where `key`=%s" , ["system/registration"] )
    if system_row is None : error_msgs.append( f"system_row None" )

    tdata = {
        "system_registration" : system_row[ "val_int" ]
    }

    return( render_template( "pages/register/main.html" , tdata = tdata ) )

@ROUTES.route( "/hx_register" , methods = [ "POST" ] )
def hx_register( ) :

    error_msgs = [ ]

    system_row = _database.db_query_select_row( "SELECT * from `system` where `key`=%s" , ["system/registration"] )
    if system_row is None : error_msgs.append( f"system_row None" )
    if system_row["val_int"]==0: raise Exception( f"system/registration not allowed" )

    form = request.form.to_dict( flat = False )

    error_msgs = [ ]

    row_data={}
    for i , ( k , v ) in enumerate( form.items( ) ) :
        if k.startswith("[") : continue
        row_data[k]=v[0].strip()

    if "email" not in form :
        error_msgs.append( f"email None" )
    else:
        if not _util.email_check( row_data["email"] ) : error_msgs.append( "Invalid email address" )

    if len( row_data.get( "name" , "" ) ) < 3 : error_msgs.append( "Invalid name" )
    if row_data.get( "name" , "" ).startswith( "_" ) : error_msgs.append( "Invalid name" )
    if len( row_data.get( "password" , "" ) ) < 8 : error_msgs.append( "Invalid password" )

    ####

    if "[_nom_form]" not in form :
        error_msgs.append( f"Registration failed" )
    else :
        if int(form["[_nom_form]"][0]) < 10 : error_msgs.append( "Registration failed" )

    ####

    if len(error_msgs)==0 :
        account_row = _database.db_query_select_row( "SELECT * from `account` where `email`=%s" , [ row_data["email"]] )
        if account_row is not None : error_msgs.append( f"Registration failed" )


    if len(error_msgs)==0 :
        row_data["email_confirm_code"]=f"{random.randint(100000, 999999)}"
        account_row = _database.insert_fromdict( "account" , row_data )




    print(form)
    ####


    tdata = {
        "error_msgs" : error_msgs 
    }

    response = make_response( render_template( "pages/register/hx_form.html" , tdata = tdata ) )

    #if len( error_msgs ) == 0 : response.headers[ "HX-Redirect" ] = url_for( ".page_admin_groups" )

    return( response )



@ROUTES.route( "/admin" , methods = [ "GET" ] )
@_common.decorator_web_login_required( "_admin" )
def page_admin( ) :
    return( render_template( "/pages/admin/main.html" ) )

@ROUTES.route( "/member" , methods = [ "GET" ] )
@_common.decorator_web_login_required( )
def page_member( ) :

    #session_data = _common.session_get( )

    #account_row = session_data.get("account_row")
    #if not account_row : raise Exception( f"account_row None" )

    #api_rows = _database.db_query_select_rows( "SELECT * from api WHERE account_id=%s LIMIT 1" , [ account_row["id"] ] )

    #cols = ["name"]

    #tdata = {
    #    "rows" : api_rows ,
    #    "cols" : cols
    #}




    return( render_template( "/pages/member/main.html" ) )

#####################################################################

@ROUTES.route( "/admin_pipelines" , methods = [ "GET" ] )
def page_admin_pipelines( ) :

    pipeline_rows = _database.db_query_select_rows( "SELECT * from pipeline ORDER by id DESC" )

    #print(pipeline_rows)

    for pipeline_row in pipeline_rows :
        pipeline_obj = _database.pipeline_object( pipeline_row )
        #pipeline_obj.print_debug( )
        pipeline_row[ "[nodes]" ] = pipeline_obj.nodes



    cols = [ "uid" , "name" , "status" , "done" , "archived" , "[nodes]" ]

    tdata = {
        "rows" : pipeline_rows ,
        "cols" : cols
    }


    return( render_template( "page_admin_pipelines.html" , tdata = tdata ) )


@ROUTES.route( "/dashboard_tasks" , methods = [ "GET" ] )
@_common.decorator_web_login_required( "_dashboard" )
def page_dashboard_tasks( ) :

    tdata = {
    }

    return( render_template( "pages/dashboard/tasks.html" , tdata = tdata ) )


@ROUTES.route( "/dashboard_pipelines" , methods = [ "GET" ] )
@_common.decorator_web_login_required( "_dashboard" )
def page_dashboard_pipelines( ) :

    tdata = {
    }

    return( render_template( "pages/dashboard/pipelines.html" , tdata = tdata ) )


#####################################################################

@ROUTES.route( "/admin/db_rolemodel_rows" , methods = [ "GET" ] )
def admin_db_rolemodel_rows( ) :

    rolemodel_rows = _database.db_query_select_rows( "SELECT id,api_id,name,enable,updateable from rolemodel order by id" )

    print(rolemodel_rows)

    for rolemodel_row in rolemodel_rows :

        rolemodel_api_id = rolemodel_row[ "api_id" ]

        if rolemodel_api_id == None : continue

        api_row = _database.db_query_select_row( "SELECT * from api where id=%s LIMIT 1" , [ rolemodel_api_id ] )
        api_name = api_row[ "name" ]
        if api_name.startswith( "test_" ) : api_name = api_name[ -10: ]

        rolemodel_row[ "[api_name]" ] = api_name
        rolemodel_row[ "[api_enable]" ] = api_row[ "enable" ]

    tdata = {
        "rolemodel_rows" : rolemodel_rows
    }
    #print(tdata)

    return( render_template( "db_rolemodel_rows.html" , tdata = tdata ) )

@ROUTES.route( "/admin/db_rolemodel_row" , methods = [ "GET" ] )
def admin_db_rolemodel_row( ) :

    rolemodel_id = _common.request_arg_int( "rolemodel_id" )

    ####

    rolemodel_row = _database.db_query_select_row( "SELECT id,api_id,name,enable,updateable from rolemodel where id=%s" , [ rolemodel_id ] )

    mport_rows = _database.db_query_select_rows( "SELECT id,port_id,direction,enable,cardinal from mport where rolemodel_id=%s order by id" , [ rolemodel_id ] )

    mpins = [ ]
    for mport_row in mport_rows :
        port_row = _database.db_query_select_row( "SELECT * from port where id=%s LIMIT 1" , [ mport_row["port_id"]] )
        port_name = port_row[ "name" ]
        mport_row[ "[port_name]" ] = port_name

        mpin_rows = _database.db_query_select_rows( "SELECT id,mport_id,unit_id from mpin where mport_id=%s order by id" , [ mport_row["id"] ] )

        for mpin_row in mpin_rows :
            unit_row = _database.db_query_select_row( "SELECT * from unit where id=%s LIMIT 1" , [ mpin_row["unit_id"]] )
            pin_row = _database.db_query_select_row( "SELECT * from pin where id=%s LIMIT 1" , [ unit_row["pin_id"]] )
            port_pin_row = _database.db_query_select_row( "SELECT * from port_pin where port_id=%s and pin_id=%s LIMIT 1" , [port_row[ "id" ] , pin_row[ "id" ] ] )
            mpin_row[ "[direction]" ] = mport_row[ "direction" ]
            mpin_row[ "[port_pin_cardinal]" ] = port_pin_row[ "cardinal" ]
            mpin_row[ "[pin_id]" ] = pin_row[ "id" ]
            mpin_row[ "[port_name/pin_name(unit_name)]" ] = port_row[ "name" ] + "/" + pin_row[ "name" ] + "(" + unit_row[ "name" ] + ")"


        mpins.append( mpin_rows)


    tdata = {
        "rolemodel_row" : rolemodel_row ,
        "mport_rows" : mport_rows ,
        "mpins" : mpins
    }

    return( render_template( "db_rolemodel_row.html" , tdata = tdata ) )

####

@ROUTES.route( "/admin/db_pipeline_rows" , methods = [ "GET" ] )
def admin_db_pipeline_rows( ) :

    pipeline_rows = _database.db_query_select_rows( "SELECT id,roleuser_id,name,status,done,archived,created_at,updated_at from pipeline order by id DESC" )

    tdata = {
        "pipeline_rows" : pipeline_rows
    }

    return( render_template( "admin_db_pipeline_rows.html" , tdata = tdata ) )

@ROUTES.route( "/admin/db_pipeline_row" , methods = [ "GET" ] )
def admin_db_pipeline_row( ) :
    pipeline_id = _common.request_arg_int( "pipeline_id" )
    pipeline_row = _database.db_query_select_row( "SELECT * from pipeline where id=%s" , [pipeline_id] )

    pipeline_object = _database.pipeline_object(pipeline_row)

    tdata = {
        "pipeline_row" : pipeline_row ,
        "pipeline" : pipeline_object
    }
    pipeline_object.print_debug()
    return( render_template( "admin_db_pipeline_row.html" , tdata = tdata ) )


@ROUTES.route( "/admin_accounts" , methods = [ "GET" ] )
@_common.decorator_web_login_required( "_admin" )
def page_admin_accounts( ) :

    rows = _database.db_query_select_rows( "SELECT * from account order by email" )
    columns = ["uid" , "email" , "name","enable","email_confirm_at","email_confirmed","email_confirmed_at","api_max"]

    tdata = {
        "time" : time.time( ) ,
        "rows" : rows ,
        "columns" : columns 
    }

    return( render_template( "pages/admin_accounts/main.html" , tdata = tdata ) )

@ROUTES.route( "/admin_account_create" , methods = [ "GET" ] )
@_common.decorator_web_login_required( "_admin" )
def page_admin_account_create( ) :


    tdata = {
        "time" : time.time( ) 
    }

    return( render_template( "pages/admin_account_create/main.html" , tdata = tdata ) )

@ROUTES.route( "/admin_group_create" , methods = [ "GET" ] )
@_common.decorator_web_login_required( "_admin" )
def page_admin_group_create( ) :


    tdata = {
        "time" : time.time( ) 
    }

    return( render_template( "pages/admin_group_create/main.html" , tdata = tdata ) )

@ROUTES.route( "/hx_admin_group_create" , methods = [ "POST" ] )
@_common.decorator_web_login_required( "_admin" )
def hx_admin_group_create( ) :

    form = request.form.to_dict( flat = False )
    print(form)

    error_msgs = [ ]

    try : input_name = _common.request_form_str( form , "name" , 3 )
    except Exception as e : error_msgs.append( f"{e}" )

    try : input_enable = _common.request_form_checkbox_single( form , "enable" )
    except Exception as e : error_msgs.append( f"{e}" )

    ####
    id = False
    if len( error_msgs ) == 0 :
        try :
            id = _database.insert_fromdict( "group" , { "name" : input_name , "enable" : input_enable } )
        except Exception as e : error_msgs.append( f"{e}" )


    ####

    tdata = {
        "time" : time.time( ) ,
        "error_msgs" : error_msgs ,
        "id" : id
    }

    response = make_response( render_template( "pages/admin_group_create/hx_form.html" , tdata = tdata ) )

    if len( error_msgs ) == 0 : response.headers[ "HX-Redirect" ] = url_for( ".page_admin_groups" )

    return( response )


@ROUTES.route( "/hx_admin_account_create" , methods = [ "POST" ] )
@_common.decorator_web_login_required( "_admin" )
def hx_admin_account_create( ) :

    form = request.form.to_dict( flat = False )
    print(form)

    error_msgs = [ ]

    try : account_email = _common.request_form_email( form , "account_email" )
    except Exception as e : error_msgs.append( f"{e}" )

    try : account_password = _common.request_form_str( form , "account_password" )
    except Exception as e : error_msgs.append( f"{e}" )

    try : account_name = _common.request_form_str( form , "account_name" , 3 )
    except Exception as e : error_msgs.append( f"{e}" )

    try : account_enable = _common.request_form_checkbox_single( form , "account_enable" )
    except Exception as e : error_msgs.append( f"{e}" )

    try : account_email_confirmed = _common.request_form_checkbox_single( form , "account_email_confirmed" )
    except Exception as e : error_msgs.append( f"{e}" )



    ####
    account_id = False
    if len( error_msgs ) == 0 :
        try :
            account_id = _database.insert_fromdict( "account" , { "email" : account_email , "password" : account_password , "name" : account_name , "enable" : account_enable , "email_confirmed" : account_email_confirmed  })
        except Exception as e : error_msgs.append( f"{e}" )


    ####

    tdata = {
        "time" : time.time( ) ,
        "error_msgs" : error_msgs ,
        "account_id" : account_id
    }

    response = make_response( render_template( "pages/admin_account_create/hx_form.html" , tdata = tdata ) )

    if len( error_msgs ) == 0 : response.headers[ "HX-Redirect" ] = url_for( ".page_admin_accounts"  )

    return( response )




@ROUTES.route( "/hx_dashboard_tasks" , methods = [ "GET" ] )
def hx_dashboard_tasks( ) :

    task_rows = _database.db_query_select_rows( "SELECT * from task where done=%s" , [ 0 ] )

    tdata = {
        "x" : datetime.now( ).isoformat( ) ,
        "y" : len( task_rows )
    }
    return( render_template( "pages/dashboard/hx_tasks.html" , tdata = tdata ) )

@ROUTES.route( "/hx_dashboard_pipelines" , methods = [ "GET" ] )
def hx_dashboard_pipelines( ) :

    rows = _database.db_query_select_rows( "SELECT * from pipeline where done=%s" , [ 0 ] )

    tdata = {
        "x" : datetime.now( ).isoformat( ) ,
        "y" : len( rows )
    }
    return( render_template( "pages/dashboard/hx_pipelines.html" , tdata = tdata ) )


@ROUTES.route( "/hx_login" , methods = [ "POST" ] )
def hx_login( ) :

    form = request.form.to_dict( flat = False )

    error_msgs = [ ]

    if "account_email" not in form : error_msgs.append( "email not found" )
    if len( form[ "account_email" ] ) != 1 : error_msgs.append( "email count != 1" )
    account_email = form[ "account_email" ][ 0 ].strip( )
    if len( account_email ) < 5 : error_msgs.append( "email to short" )

    if "account_password" not in form : error_msgs.append( "password not found" )
    if len( form[ "account_password" ] ) != 1 : error_msgs.append( "password count != 1" )
    account_password = form[ "account_password" ][ 0 ].strip( )
    if len( account_password ) < 5 : error_msgs.append( "password to short" )

    ####

    account_row = { }
    account_name = None
    if len( error_msgs ) == 0 :
        password = _util.hash_str( account_password )
        account_row = _database.db_query_select_row( "SELECT * from account WHERE email=%s AND password=%s LIMIT 1" , [ account_email , password ] )
        if account_row == None :
            error_msgs.append( "An error occurred. Please try again later." )
        else :
            account_name = account_row[ "name" ]


    if len( error_msgs ) == 0 :
        if account_row["enable"]==0: error_msgs.append( "Account not enabled" )


    session_data = { }
    if len( error_msgs ) == 0 :
        session_key = request.cookies.get( "key" , "" ).strip( )
        if len( session_key ) == 64 :
            _database.db_query_delete( "DELETE FROM session WHERE `key`=%s LIMIT 1" , [ session_key ] )

            remote_ip = request.headers.get( "X-Forwarded-For" )
            if not remote_ip : remote_ip = request.remote_addr

            session_data = {
                "time" : time.time( ) ,
                "ip" : remote_ip ,
                "ua" : request.headers.get( "User-Agent" ) ,
                "loggedin" : True ,
                "account_row" : account_row
            }
            _database.insert_fromdict( "session" , { "key" : session_key , "data" : json.dumps( session_data , default = str ) })

    ####

    tdata = {
        "k1" : time.time( ) ,
        "error_msgs" : error_msgs ,
        "account_name" : account_name
    }

    response = make_response( render_template( "pages/login/hx_login.html" , tdata = tdata ) )

    ####

    if session_data.get( "loggedin" , False ) :

        if account_name == "_admin" :
            url_redirect = url_for( ".page_admin" )
        else :
            url_redirect = url_for( ".page_member" )

        response.headers[ "HX-Redirect" ] = url_redirect

    ####

    return( response )


@ROUTES.route( "/hx_admin_account" , methods = [ "GET" ] )
@_common.decorator_web_login_required( "_admin" )
def hx_admin_account( ) :

    account_uid = _common.request_arg_str( "account_uid" )
    if account_uid == "" : raise Exception( f"account_uid blank" )

    account_row = _database.db_query_select_row( "SELECT * from account WHERE uid=%s LIMIT 1" , [ account_uid ] )
    if account_row is None : raise Exception( f"account_row None" )

    api_rows = _database.db_query_select_rows( "SELECT * from api WHERE account_id=%s" , [ account_row["id"] ] )

    columns = ["uid","name","enable"]

    tdata = {
        "k1" : time.time( ) ,
        "account_row" : account_row ,
        "rows" : api_rows ,
        "columns" : columns
    }

    #print(tdata)

    return( render_template( "pages/admin/hx_admin_account.html" , tdata = tdata ) )


@ROUTES.route( "/member_apis" , methods = [ "GET" ] )
@_common.decorator_web_login_required( )
def page_member_apis( ) :

    session_data = _common.session_get( )

    account_row = session_data.get("account_row")
    if not account_row : raise Exception( f"account_row None" )


    api_rows = _database.db_query_select_rows( "SELECT * from `api` where `account_id`=%s ORDER by `name`",[account_row["id"]] )

    for api_row in api_rows :
        api_role_row = _database.db_query_select_row( "SELECT * from `api_role` WHERE api_id=%s LIMIT 1" , [api_row["id"]])
        role_row = _database.db_query_select_row( "SELECT * from `role` WHERE id=%s LIMIT 1" , [api_role_row["role_id"]])
        api_row["[role_name]"]=role_row["name"]

    columns = ["uid","[role_name]","name","token","enable"]

    flag_apimax = len( api_rows ) >= account_row[ "api_max" ]

    tdata = {
        "k1" : time.time( ) ,
        "rows" : api_rows ,
        "columns" : columns ,
        "flag_apimax" : flag_apimax
    }

    #print(tdata)

    return( render_template( "pages/member_apis/main.html" , tdata = tdata ) )


@ROUTES.route( "/member_logs" , methods = [ "GET" ] )
@_common.decorator_web_login_required( )
def page_member_logs( ) :

    session_data = _common.session_get( )

    account_row = session_data.get("account_row")
    if not account_row : raise Exception( f"account_row None" )

    rows = _database.db_query_select_rows( "SELECT * from `log` where `account_id`=%s ORDER by id DESC LIMIT 10",[account_row["id"]] )

    columns = ["event","data"]

    tdata = {
        "rows" : rows ,
        "columns" : columns 
    }

    #print(tdata)

    return( render_template( "pages/member_logs/main.html" , tdata = tdata ) )


@ROUTES.route( "/admin_models" , methods = [ "GET" ] )
@_common.decorator_web_login_required( "_admin" )
def page_admin_models( ) :

    rows = _database.db_query_select_rows( "SELECT * from `rolemodel`" )

    columns = [ "uid" , "name" , "category" , "enable" , "updateable" ]

    tdata = {
        "k1" : time.time( ) ,
        "rows" : rows ,
        "columns" : columns
    }

    #print(tdata)

    return( render_template( "pages/admin_models/main.html" , tdata = tdata ) )

@ROUTES.route( "/admin_model_read" , methods = [ "GET" ] )
@_common.decorator_web_login_required( "_admin" )
def page_admin_model_read( ) :

    uid = _common.request_arg_str( "uid" )

    row = _database.db_query_select_row( "SELECT * from `rolemodel` WHERE uid=%s LIMIT 1" , [ uid ] )
    if row is None : raise Exception( f"row None" )

    tdata = {
        "row" : row 
    }

    #print(tdata)

    return( render_template( "pages/admin_model_read/main.html" , tdata = tdata ) )


@ROUTES.route( "/admin_model_update" , methods = [ "GET" ] )
@_common.decorator_web_login_required( "_admin" )
def page_admin_model_update( ) :

    uid = _common.request_arg_str( "uid" )

    row = _database.db_query_select_row( "SELECT * from `rolemodel` WHERE uid=%s LIMIT 1" , [ uid ] )
    if row is None : raise Exception( f"row None" )

    tdata = {
        "k1" : time.time( ) ,
        "row" : row 
    }

    #print(tdata)

    return( render_template( "pages/admin_model_update/main.html" , tdata = tdata ) )


@ROUTES.route( "/hx_admin_model_update" , methods = [ "POST" ] )
@_common.decorator_web_login_required( "_admin" )
def hx_admin_model_update( ) :

    uid = _common.request_arg_str( "uid" )

    # FIXME TODO check if id is available and allowed
    #row = _database.db_query_select_row( "SELECT * from `group` WHERE id=%s LIMIT 1" , [id])
    #if row is None : raise Exception( f"row None" )

    ####

    form = request.form.to_dict( flat = False )
    print(form)

    ####
    row_data = { }

    for i , ( k , v ) in enumerate( form.items( ) ) :
        if k.startswith("[") : continue
        row_data[k]=v[0]


    if "enable" not in row_data : row_data["enable"]=0
    if "updateable" not in row_data : row_data["updateable"]=0

    #print(row_data)

    _database.update_fromdict( "rolemodel" , uid , row_data , cid = "uid" )
    ####

    tdata = {
        "k1" : time.time( ) 
    }

    #print(tdata)

    response = make_response( render_template( "pages/admin_model_update/hx_form.html" , tdata = tdata ) )

    response.headers[ "HX-Redirect" ] = url_for( ".page_admin_model_read" , uid = uid )

    ####

    return( response )


@ROUTES.route( "/admin_apis" , methods = [ "GET" ] )
@_common.decorator_web_login_required( "_admin" )
def page_admin_apis( ) :

    api_rows = _database.db_query_select_rows( "SELECT * from `api`" )

    for api_row in api_rows :
        account_row = _database.db_query_select_row( "SELECT * from `account` WHERE id=%s LIMIT 1" , [api_row["account_id"]])
        api_row["[account_email]"]=account_row["email"]
        api_row["[account_name]"]=account_row["name"]
        api_role_row = _database.db_query_select_row( "SELECT * from `api_role` WHERE api_id=%s LIMIT 1" , [api_row["id"]])
        role_row = _database.db_query_select_row( "SELECT * from `role` WHERE id=%s LIMIT 1" , [api_role_row["role_id"]])
        api_row["[role_name]"]=role_row["name"]

    columns = [ "uid" , "[account_email]" ,"[account_name]", "[role_name]" , "name" , "token" , "enable" , "ip" , "ip_update" ]

    tdata = {
        "k1" : time.time( ) ,
        "rows" : api_rows ,
        "columns" : columns
    }

    #print(tdata)

    return( render_template( "pages/admin_apis/main.html" , tdata = tdata ) )


@ROUTES.route( "/admin_groups" , methods = [ "GET" ] )
@_common.decorator_web_login_required( "_admin" )
def page_admin_groups( ) :

    rows = _database.db_query_select_rows( "SELECT * from `group`" )
    columns = [ "uid" , "name" , "enable" ]

    tdata = {
        "k1" : time.time( ) ,
        "rows" : rows ,
        "columns" : columns
    }

    #print(tdata)

    return( render_template( "pages/admin_groups/main.html" , tdata = tdata ) )

@ROUTES.route( "/admin_group_read" , methods = [ "GET" ] )
@_common.decorator_web_login_required( "_admin" )
def page_admin_group_read( ) :

    uid = _common.request_arg_str( "uid" )

    row = _database.db_query_select_row( "SELECT * from `group` WHERE uid=%s LIMIT 1" , [ uid ] )
    if row is None : raise Exception( f"api_row None" )

    tdata = {
        "k1" : time.time( ) ,
        "row" : row 
    }

    #print(tdata)

    return( render_template( "pages/admin_group_read/main.html" , tdata = tdata ) )


@ROUTES.route( "/admin_api_read" , methods = [ "GET" ] )
@_common.decorator_web_login_required( "_admin" )
def page_admin_api_read( ) :

    api_uid = _common.request_arg_str( "api_uid" )

    api_row = _database.db_query_select_row( "SELECT * from `api` WHERE uid=%s LIMIT 1" , [api_uid])

    if api_row is None : raise Exception( f"api_row None" )



    api_row["[group_names]"]=[]
    api_group_rows = _database.db_query_select_rows( "SELECT * from `api_group` WHERE api_id=%s" , [api_row['id']])

    #print(f"{api_group_rows=}")

    for api_group_row in api_group_rows :
        group_row = _database.db_query_select_row( "SELECT * from `group` WHERE id=%s LIMIT 1" , [api_group_row['group_id']])
        api_row["[group_names]"].append(group_row["name"])


    tdata = {
        "k1" : time.time( ) ,
        "row" : api_row 
    }

    #print(tdata)

    return( render_template( "pages/admin_api_read/main.html" , tdata = tdata ) )


@ROUTES.route( "/admin_api_update" , methods = [ "GET" ] )
@_common.decorator_web_login_required( "_admin" )
def page_admin_api_update( ) :

    api_uid = _common.request_arg_str( "api_uid" )

    api_row = _database.db_query_select_row( "SELECT * from `api` WHERE uid=%s LIMIT 1" , [api_uid])

    if api_row is None : raise Exception( f"api_row None" )

    api_row["[group_names]"]=[]
    api_group_rows = _database.db_query_select_rows( "SELECT * from `api_group` WHERE api_id=%s" , [api_row['id']])

    for api_group_row in api_group_rows :
        group_row = _database.db_query_select_row( "SELECT * from `group` WHERE id=%s LIMIT 1" , [api_group_row['group_id']])
        api_row["[group_names]"].append(group_row["name"])


    group_rows = _database.db_query_select_rows( "SELECT * from `group`" )

    tdata = {
        "k1" : time.time( ) ,
        "row" : api_row ,
        "group_rows" : group_rows
    }

    #print(tdata)

    return( render_template( "pages/admin_api_update/main.html" , tdata = tdata ) )

@ROUTES.route( "/admin_group_update" , methods = [ "GET" ] )
@_common.decorator_web_login_required( "_admin" )
def page_admin_group_update( ) :

    uid = _common.request_arg_str( "uid" )

    row = _database.db_query_select_row( "SELECT * from `group` WHERE uid=%s LIMIT 1" , [ uid ] )
    if row is None : raise Exception( f"api_row None" )

    tdata = {
        "k1" : time.time( ) ,
        "row" : row 
    }

    #print(tdata)

    return( render_template( "pages/admin_group_update/main.html" , tdata = tdata ) )


@ROUTES.route( "/hx_admin_group_update" , methods = [ "POST" ] )
@_common.decorator_web_login_required( "_admin" )
def hx_admin_group_update( ) :

    uid = _common.request_arg_str( "uid" )

    # FIXME TODO check if id is available and allowed
    #row = _database.db_query_select_row( "SELECT * from `group` WHERE id=%s LIMIT 1" , [id])
    #if row is None : raise Exception( f"row None" )


    ####

    form = request.form.to_dict( flat = False )
    print(form)

    ####
    row_data = { }

    for i , ( k , v ) in enumerate( form.items( ) ) :
        if k.startswith("[") : continue
        row_data[k]=v[0]

    if "enable" not in row_data : row_data["enable"]=0

    #print(row_data)

    _database.update_fromdict( "group" , uid , row_data , cid = "uid" )
    ####

    tdata = {
        "k1" : time.time( ) 
    }

    #print(tdata)

    response = make_response( render_template( "pages/admin_group_update/hx_form.html" , tdata = tdata ) )

    response.headers[ "HX-Redirect" ] = url_for( ".page_admin_group_read" , uid = uid )

    ####

    return( response )

@ROUTES.route( "/hx_admin_api_update" , methods = [ "POST" ] )
@_common.decorator_web_login_required( "_admin" )
def hx_admin_api_update( ) :

    api_uid = _common.request_arg_str( "api_uid" )

    api_row = _database.db_query_select_row( "SELECT * from `api` WHERE uid=%s LIMIT 1" , [api_uid])
    if api_row is None : raise Exception( f"api_row None" )

    api_id = api_row[ "id" ]

    ####

    form = request.form.to_dict( flat = False )
    print(form)

    ####
    row_data = { }

    for i , ( k , v ) in enumerate( form.items( ) ) :
        if k.startswith("[") : continue
        row_data[k]=v[0]

    if "ip_update" not in row_data : row_data["ip_update"]=0
    if "enable" not in row_data : row_data["enable"]=0

    print(row_data)

    _database.update_fromdict( "api" , api_uid , row_data , cid = "uid")
    ####

    incoming_group_ids = [ ]
    if "[group_ids]" in form : incoming_group_ids = form["[group_ids]"]
    incoming_group_ids = list(map(int, incoming_group_ids))

    print(incoming_group_ids)
    api_group_rows = _database.db_query_select_rows( "SELECT * from `api_group` WHERE api_id=%s" , [ api_id ] )

    current_group_ids = [ ]
    for api_group_row in api_group_rows : current_group_ids.append( api_group_row[ "group_id" ] )

    print(current_group_ids)

    for current_group_id in current_group_ids :
        if current_group_id not in incoming_group_ids :
            _database.db_query_delete( "DELETE FROM api_group WHERE `group_id`=%s AND api_id=%s LIMIT 1" , [ current_group_id , api_id ] )

    for incoming_group_id in incoming_group_ids :
        if incoming_group_id not in current_group_ids :
            _database.insert_fromdict( "api_group" , { "api_id" : api_id , "group_id" : incoming_group_id } )




    ####

    tdata = {
        "k1" : time.time( ) 
    }

    #print(tdata)

    response = make_response( render_template( "pages/admin_api_update/hx_form.html" , tdata = tdata ) )

    response.headers[ "HX-Redirect" ] = url_for( ".page_admin_api_read" , api_uid=api_uid)

    ####

    return( response )



@ROUTES.route( "/member_api_create" , methods = [ "GET" ] )
@_common.decorator_web_login_required( )
def page_member_api_create( ) :
    return( render_template( "pages/member_api_create/main.html" ) )


@ROUTES.route( "/hx_member_api_create" , methods = [ "POST" ] )
@_common.decorator_web_login_required( )
def hx_member_api_create( ) :

    form = request.form.to_dict( flat = False )
    print(form)

    error_msgs = [ ]

    try : api_name = _common.request_form_str( form , "api_name" , 1 )
    except Exception as e : error_msgs.append( f"{e}" )

    try : role_name = _common.request_form_str( form , "role_name" , 1 )
    except Exception as e : error_msgs.append( f"{e}" )

    #print(f"{api_name=} {role_name=}")

    if role_name not in [ "user" , "model" ] : error_msgs.append( f"role error" )

    role_row = _database.db_query_select_row( "SELECT * from `role` where `name`=%s" , [ role_name ] )
    if role_row is None : error_msgs.append( f"role_row None" )

    default_group_row = _database.db_query_select_row( "SELECT * from `group` where `name`=%s" , [ "default" ] )
    if default_group_row is None : error_msgs.append( f"default_group_row None" )

    api_row = None
    if len( error_msgs ) == 0 : 

        session_data = _common.session_get( )

        account_row = session_data.get("account_row")
        if not account_row : raise Exception( f"account_row None" )

        #api_enable = 0
        #if role_name == "user" : api_enable = 1

        #api_id = _database.insert_fromdict( "api" , { "account_id" : account_row["id"] , "name" : api_name , "ip":_common.request_ip( ) , "enable" : api_enable } )
        api_id = _database.insert_fromdict( "api" , { "account_id" : account_row["id"] , "name" : api_name , "ip":_common.request_ip( ) , "enable" : 1 , "ip_update" : 1 } )


        api_role_id = _database.insert_fromdict( "api_role" , { "api_id" : api_id , "role_id" : role_row[ "id" ] } )
        api_group_id = _database.insert_fromdict( "api_group" , { "api_id" : api_id , "group_id" : default_group_row["id"] } )

        if role_name == "user" : 
            roleuser_id = _database.insert_fromdict( "roleuser" , { "api_id" : api_id } )

        api_row = _database.db_query_select_row( "SELECT * from `api` where `id`=%s" , [api_id] )



    tdata = {
        "k1" : time.time( ) ,
        "error_msgs" : error_msgs ,
        "api_row" : api_row,
        "url_root" : request.url_root
    }

    #print(tdata)



    return( render_template( "pages/member_api_create/hx_form.html" , tdata = tdata ) )



@ROUTES.route( "/admin_settings" , methods = [ "GET" ] )
@_common.decorator_web_login_required( )
def page_admin_settings( ) :

    error_msgs = [ ]

    system_row = _database.db_query_select_row( "SELECT * from `system` where `key`=%s" , ["system/id"] )
    if system_row is None : error_msgs.append( f"system_row None" )
    system_id=system_row[ "val_str" ]

    system_row = _database.db_query_select_row( "SELECT * from `system` where `key`=%s" , ["system/registration"] )
    if system_row is None : error_msgs.append( f"system_row None" )
    system_registration=system_row[ "val_int" ]    

    tdata = {
        "k1" : time.time( ) ,
        "error_msgs" : error_msgs ,
        "system/id" : system_id,
        "system/registration" : system_registration
    }


    return( render_template( "pages/admin_settings/main.html" , tdata = tdata ) )

@ROUTES.route( "/hx_admin_settings_form_system_id" , methods = [ "POST" ] )
@_common.decorator_web_login_required( "_admin" )
def hx_admin_settings_form_system_id( ) :

    form = request.form.to_dict( flat = False )
    print( form )

    try : val_str = _common.request_form_str( form , "val_str" , 1 )
    except Exception as e : error_msgs.append( f"{e}" )

    row_data = {
        "val_str" : val_str
    }
    _database.update_fromdict( "system" , "system/id" , row_data , cid = "key" )

    return( render_template( "pages/admin_settings/hx_form.html" ) )


@ROUTES.route( "/hx_admin_settings_ports" , methods = [ "POST" ] )
@_common.decorator_web_login_required( "_admin" )
def hx_admin_settings_ports( ) :

    f = request.files['file']
    f.save("/tmp/"+secure_filename(f.filename))

    with open("/tmp/ports.json") as f:
        ports = json.loads(f.read())

    port_ids = [ ]

    for port_i , ( port_name , port_val ) in enumerate( ports.items( ) ) :

        row_data = { "name" : port_name , "description" : port_val.get( "description" ) }

        port = _database.db_query_select_row( "SELECT * from `port` where `name`=%s LIMIT 1" , [ port_name ] )

        if port is None :
            port_id = _database.insert_fromdict( "port" , row_data )
            print( f"CREATED {port_name=}" )
        else :
            port_id = port[ "id" ]
            _database.update_fromdict( "port" , port_id , row_data )
            print( f"UPDATED {port_name=}" )

        port_ids.append( port_id )

        _database.db_query_delete( "DELETE FROM `port_pin` WHERE `port_id`=%s" , [ port_id ] )

        print( f"{port_id=}" )

        if "pins" not in port_val : continue

        for pin_i , ( pin_name , pin_val ) in enumerate( port_val["pins"].items( ) ) :
            pin_row = _database.db_query_select_row( "SELECT * from `pin` where `name`=%s LIMIT 1" , [ pin_name ] )
            if pin_row is None :
                raise Exception( f"ERROR: PIN NOT FOUND {pin_name=}" )

            port_pin_data = { "port_id" : port_id , "pin_id" : pin_row[ "id" ] , "cardinal" : pin_val.get( "cardinal" , 1 ) }
            _database.insert_fromdict( "port_pin" , port_pin_data )


    ####

    rows = _database.db_query_select_rows( "SELECT * from `port`" )
    for row in rows :
        if row[ "id" ] not in port_ids :
            _database.db_query_delete( "DELETE FROM `port` WHERE `id`=%s LIMIT 1" , [ row[ "id" ] ] )

    ####

    return( render_template( "pages/admin_settings/hx_form.html" ) )



@ROUTES.route( "/hx_admin_settings_pins" , methods = [ "POST" ] )
@_common.decorator_web_login_required( "_admin" )
def hx_admin_settings_pins( ) :

    f = request.files['file']
    f.save("/tmp/"+secure_filename(f.filename))

    with open("/tmp/pins.json") as f:
        pins = json.loads(f.read())

    pin_ids = [ ]

    for pin_i , ( pin_name , pin_val ) in enumerate( pins.items( ) ) :

        row_data = { "name" : pin_name , "description" : pin_val.get( "description" ) , "type" : pin_val.get( "type" ) }

        pin = _database.db_query_select_row( "SELECT * from `pin` where `name`=%s LIMIT 1" , [ pin_name ] )

        if pin is None :
            pin_id = _database.insert_fromdict( "pin" , row_data )
            print( f"CREATED {pin_name=}" )
        else :
            pin_id = pin[ "id" ]
            _database.update_fromdict( "pin" , pin_id , row_data )
            print( f"UPDATED {pin_name=}" )

        pin_ids.append( pin_id )

        print( f"{pin_id=}" )

        ####

        flag_default_unit_i = 0
        for unit_i , ( unit_name , unit_val ) in enumerate( pin_val[ "units" ].items( ) ) :
            if unit_val.get( "default" , 0 ) == 1 :
                flag_default_unit_i = unit_i
                break

        ####

        unit_ids = [ ]

        for unit_i , ( unit_name , unit_val ) in enumerate( pin_val[ "units" ].items( ) ) :

            unit_default = unit_i == flag_default_unit_i

            row_data = { "pin_id" : pin_id , "name" : unit_name , "description" : unit_val.get( "description" ) , "symbol" : unit_val.get( "symbol" ) , "default" : unit_default }

            unit = _database.db_query_select_row( "SELECT * from `unit` where pin_id=%s and `name`=%s LIMIT 1" , [ pin_id, unit_name ] )

            if unit is None :
                unit_id = _database.insert_fromdict( "unit" , row_data )
                print( f"CREATED {unit_name=}" )
            else :
                unit_id = unit[ "id" ]
                _database.update_fromdict( "unit" , unit_id , row_data )
                print( f"UPDATED {unit_name=}" )

            unit_ids.append( unit_id )

        ####

        rows = _database.db_query_select_rows( "SELECT * from `unit` where `pin_id`=%s" , [ pin_id ] )
        for row in rows :
            if row[ "id" ] not in unit_ids :
                _database.db_query_delete( "DELETE FROM `unit` WHERE `id`=%s LIMIT 1" , [ row[ "id" ] ] )

        ####


    ####

    rows = _database.db_query_select_rows( "SELECT * from `pin`" )
    for row in rows :
        if row[ "id" ] not in pin_ids :
            _database.db_query_delete( "DELETE FROM `pin` WHERE `id`=%s LIMIT 1" , [ row[ "id" ] ] )

    ####

    return( render_template( "pages/admin_settings/hx_form.html" ) )

@ROUTES.route( "/hx_admin_settings_form_system_registration" , methods = [ "POST" ] )
@_common.decorator_web_login_required( "_admin" )
def hx_admin_settings_form_system_registration( ) :

    form = request.form.to_dict( flat = False )
    print( form )

    try : val_int = _common.request_form_int( form , "val_int" , default = 0 )
    except Exception as e : error_msgs.append( f"{e}" )

    row_data = {
        "val_int" : val_int
    }
    _database.update_fromdict( "system" , "system/registration" , row_data , cid = "key" )

    return( render_template( "pages/admin_settings/hx_form.html" ) )


