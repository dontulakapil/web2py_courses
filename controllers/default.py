# -*- coding: utf-8 -*- 

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  

#def index():
 #   """
  #  example action using the internationalization operator T and flash
   # rendered by views/default/index.html or views/generic.html
    #"""
    #response.flash = T('Welcome to web2py')
    #return dict(message=T('Hello World'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()
@auth.requires_login()
def index():
    courses=db().select(db.courses.ALL)
    return dict(courses=courses)

def insert():
    form=SQLFORM(db.courses)
    if form.accepts(request.vars,session):
        response.flash = 'course is posted'
    return(dict(form=form))
def show():
    k=request.args(0)
    courses=db(db.courses.courses_id==k).select()
    ta=db(db.TA.courses_id==courses[0].id).select()
    asignments=db(db.assignment.courses_id==courses[0].id).select()
    return dict(courses=courses,ta=ta,asignments=asignments)
def delete():
    k=request.args(0)
    crud.delete(db.courses,k,next=URL(r=request,f="index"))
    return
def addas():
    form=SQLFORM(db.assignment)
    form.vars.courses_id=request.args(0)
    if form.accepts(request.vars,session):
        response.flash = 'asignment posted'
    return(dict(form=form))
def addinmem():
    form=SQLFORM(db.auth_membership)
    if form.accepts(request.vars,session):
        redirect(URL(r=request,f='index'))
    return(dict(form=form))    
def addinauth():
    form=SQLFORM(db.auth_user)
    if form.accepts(request.vars,session):
        redirect(URL(r=request,f=addinmem))
    return(dict(form=form))
def addta():
    form=SQLFORM(db.TA)
    if form.accepts(request.vars,session):
        redirect(URL(r=request,f=addinauth))
    return(dict(form=form))
