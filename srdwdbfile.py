#!/usr/bin/env nix-shell
#!nix-shell -i python -p python27Packages.flask python27Packages.sqlite3
from flask import Flask, request, jsonify, make_response
import sqlite3
#####################################################################################################################################################################################
#Script Name - srdfile.py                                                                                                                                                           #
#A python script using flask framework                                                                                                                                              #
#Name srdfile indicates :                                                                                                                                                           #
# s    ==> save                                                                                                                                                                     #
# r    ==> retrieve                                                                                                                                                                 #
# d    ==> delete                                                                                                                                                                   #
# file ==> Indicating the object of operation                                                                                                                                       #
#####################################################################################################################################################################################
#
#This script implements a local web server in flask, which is meant for development and testing purpose only. And should not be used for production
#It uses port "8080", so as to avoid conflict with default Apache (httpd) port
#The test URL is accessible at http://localhost:8080/flist 
#This script implements API (REST API) web service
#The resources exposed by this service is called flist, indicating file listing
#And uses the following HTTP methods:
# GET    URI "http://localhost:8080/flist/all"        --- This method gets all of availalble file list.
# GET    URI "http://localhost:8080/flist/<filename>  --- This method gets the file as specified by the filename parameter
# POST   URI "http://localhost:8080/flist             --- This method uploads a file provided in json format
# DELETE URI "http://localhost:8080/flist/<filename>  --- This method deletes a file as specified by the filename parameter
#################################################################################################################################################################################### 
#
#This script is a direct executable in the nixos environment.
#That is, it can invoked directly calling the script with nix-shell command, as below:
#(As a normal user execute) nix-shell /webroot/srdwdbfile.py    (i.e., the script file name with its location
#Now the REST API web service can be accessed either by curl or in a browser
#as per the above URIs (Only GET methods is directly available in the browser
#The following curl syntax provides a means to operate on the REST API services in command mode:
#
# GET     ==> To retrieve the whole file list:
#
# curl -X GET http://localhost:8080/flist/all
#
# GET     ==> To retrieve a single file with filename parameter:
#
# curl -X GET http://localhost:8080/flist/<filename>
#
# POST    ==> To upload a new file:
#
# curl -i -H "Content-Type: application/json" -X POST -d '{"name": "filename"}' http://localhost:8080/flist
#
#
# DELETE  ==> To delete a file by name:
#
# curl -i -H "Content-Type: application/json" -X DELETE http://localhost:8080/flist/<filename>
# or
# curl -i -X DELETE http://localhost:8080/flist/<filename>
#
###################################################################################################################################################################################
#
# This version of the script uses a sqlite3 database DB for file upload, delete and listing demonstration
#
################################################################################################################################################################################## 
#
#Here the regular "environment/path" specification line is modified to include the nixos specific environment variables
#And then the various flask modules gets called automatically on invocation
#
##################################################################################################################################################################################

#srdfile is an object, which instantiates the Flask class

srdfile = Flask(__name__)

# A Sqlite3 Database location specifier

SRDFDATABASE = '/webroot/srdfData.db'


def srdfDB_open():
    #Function to establish connection to database
    try:
        srdfdbCONN = sqlite3.connect(SRDFDATABASE)
        return(srdfdbCONN)
    except:
        return('DBConnectFailed')

def srdfDB_read(TRNAME):
    # Function to read table data
    try:
        if (TRNAME == 'all' or TRNAME == '*' or TRNAME == 'ALL' or TRNAME == 'All'):
            srdfDBQuery = ("SELECT * from srdfiles;")
        else:
            srdfDBQuery = ("SELECT * from srdfiles where name='%s';")%(TRNAME)
        srdfDBRconn = srdfDB_open()
        srdfDBRcursor = srdfDBRconn.cursor()
        srdfDBRcursor.execute(srdfDBQuery)
        srdfDBRrows = srdfDBRcursor.fetchall()
        return jsonify({ 'name': [i[0] for i in srdfDBRrows]})
    except:
        return("ReadError")

def srdfDB_update(TUNAME):
    #Function to insert / update table data
    try:
        srdfDBURQuery = ("Select * from srdfiles where name='%s';")%(TUNAME)
        srdfDBUQuery = ("INSERT into srdfiles (name) values ('%s');")%(TUNAME)
        srdfDBUconn = srdfDB_open()
        srdfDBUcursor = srdfDBUconn.cursor()
        srdfDBUcursor.execute(srdfDBURQuery)
        srdfDBURrows = srdfDBUcursor.fetchall()
        if (len(srdfDBURrows) == 0):
            srdfDBUcursor.execute(srdfDBUQuery)
            srdfDBUconn.commit()
            srdfDBUcursor.execute(srdfDBURQuery)
            return jsonify({ 'name': [i[0] for i in srdfDBUcursor.fetchall()]})
        else:
            return('FileInDB')
    except:
        return('UploadError')

def srdfDB_delete(TDNAME):
    #Function to delete table data
    try:
        srdfDBDRQuery = ("Select * from srdfiles where name='%s';")%(TDNAME)
        srdfDBDQuery = ("DELETE from srdfiles where name='%s';")%(TDNAME)
        srdfDBDconn = srdfDB_open()
        srdfDBDcursor = srdfDBDconn.cursor()
        srdfDBDcursor.execute(srdfDBDRQuery)
        srdfDBDRrows = srdfDBDcursor.fetchall()
        if (len(srdfDBDRrows) == 0):
            return('FileNotInDB')
        else:
            srdfDBDcursor.execute(srdfDBDQuery)
            srdfDBDconn.commit()
            srdfDBDcursor.execute(srdfDBDRQuery)
            return jsonify({ 'name': [i[0] for i in srdfDBDcursor.fetchall()]})
    except:
        return('DeleteError')




def wrong_del(Dfname):
    #Function to show wrong filename specification on DELETE method call
    return make_response(jsonify({'name' : 'Wrong File Name'}))

def wrong_input():
    #Function to show wrong filename specification on POST (Upload) method call
    return make_response(jsonify({'name' : 'Wrong Parameter'}))


def wrong_choice(eRROr):
    #Function to show wrong filename specification on GET method call
    return make_response(jsonify({eRROr: 'No File found'}))


@srdfile.route('/flist/<fNAME>', methods = [ 'GET' ] ) 
def srdf(fNAME):
    #Function to display file list
    return (srdfDB_read(fNAME))

@srdfile.route('/flist', methods = [ 'POST' ] )
def srdfIN():
    #Function to upload a file
    if not request.json or not 'name' in request.json:
        return(wrong_input())
    else:
        return(srdfDB_update(request.json.get('name',"")))


@srdfile.route('/flist/<DFNAME>', methods = [ 'DELETE' ] )
def srdfDEL(DFNAME):
    #Function to delete a given filename
    return(srdfDB_delete(DFNAME))

if __name__ == "__main__":
    srdfile.run(host='0.0.0.0',port=8080,debug=True)

