# -*- coding: utf-8 -*- 

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db=db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db=MEMDB(Client())
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for 
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## comment/uncomment as needed

from gluon.tools import *
auth=Auth(globals(),db)                      # authentication/authorization
auth.settings.hmac_key='sha512:e1c5f5b9-4c15-4cfc-b50f-802054f6c6d9'
auth.define_tables()                         # creates all needed tables
crud=Crud(globals(),db)                      # for CRUD helpers using auth
service=Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc

# crud.settings.auth=auth                      # enforces authorization on crud
# mail=Mail()                                  # mailer
# mail.settings.server='smtp.gmail.com:587'    # your SMTP server
# mail.settings.sender='you@gmail.com'         # your email
# mail.settings.login='username:password'      # your credentials or None
# auth.settings.mailer=mail                    # for user email verification
# auth.settings.registration_requires_verification = True
# auth.settings.registration_requires_approval = True
# auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
# auth.settings.reset_password_requires_verification = True
# auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'
## more options discussed in gluon/tools.py
#########################################################################

#########################################################################
## Define your tables below, for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
db.define_table('courses',
                    Field('course','string'),                
                    Field('courses_id','string'),
                    Field('credits','integer'),
                    Field('faculty','string'))
db.courses.course.requires = IS_NOT_EMPTY()
db.courses.courses_id.requires = IS_NOT_EMPTY()
db.courses.credits.requires = IS_NOT_EMPTY()
db.courses.faculty.requires = IS_NOT_EMPTY()
db.define_table('TA',              
                    Field('courses_id',db.courses),
                    Field('ta_name','string'))
db.TA.courses_id.requires = IS_IN_DB(db,'courses.id','courses.courses_id')
db.TA.ta_name.requires = IS_NOT_EMPTY()
db.define_table('assignment',              
                    Field('courses_id',db.courses),
                    Field('assignment_name','string'),
                    Field('assignment_discription','text'))
db.assignment.assignment_name.requires = IS_NOT_EMPTY()
db.assignment.courses_id.requires = (IS_IN_DB(db,'courses.id','courses.courses_id'))
db.courses.id.writable = db.courses.id.readable = False
db.TA.id.writable = db.TA.id.readable = False
db.assignment.id.writable = db.assignment.id.readable = False
db.assignment.courses_id.writable = db.assignment.courses_id.readable = False
db.courses.courses_id.requires = IS_NOT_IN_DB(db,'courses.id','courses.courses_id')
