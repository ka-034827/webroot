#!/usr/bin/env nix-shell
#!nix-shell -i python -p python27Packages.flask
from flask import Flask, request, jsonify, make_response
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
#(As a normal user execute) nix-shell /webroot/srdfile.py    (i.e., the script file name with its location
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
# This version of the script uses an in memory data structure for file upload, delete and listing demonstration
#
# The next version of this script implements a database (sqlite3) implementation of the same
#
################################################################################################################################################################################## 
#
#Here the regular "environment/path" specification line is modified to include the nixos specific environment variables
#And then the various flask modules gets called automatically on invocation
#
##################################################################################################################################################################################

#srdfile is an object, which instantiates the Flask class

srdfile = Flask(__name__)

# A in memory data-structure for demonstrating REST API web services

srdFList = [ {'name': 'afile'}, {'name': 'aAfile'},{'name': 'bfile'},{'name': 'bBfile'},{'name': 'cfile'} ]


def wrong_del(Dfname):
    #Function to show wrong filename specification on DELETE method call
    return make_response(jsonify({'name' : 'Wrong File Name'}))

def wrong_input():
    #Function to show wrong filename specification on POST (Upload) method call
    return make_response(jsonify({'name' : 'Wrong File Provided'}))


def wrong_choice(eRROr):
    #Function to show wrong filename specification on GET method call
    return make_response(jsonify({eRROr: 'No File found'}))


@srdfile.route('/flist/<fNAME>', methods = [ 'GET' ] ) 
def srdf(fNAME):
    #Function to display file list
    if fNAME == '*' or fNAME == 'all' or fNAME == 'ALL':
        return jsonify({'flist': srdFList})
    srdOUTFile = [ outFILE1 for outFILE1 in srdFList if outFILE1['name'] == fNAME ]
    if len(srdOUTFile) == 0:
        return(wrong_choice(fNAME))
    else:
        return jsonify({'flist': srdOUTFile})

@srdfile.route('/flist', methods = [ 'POST' ] )
def srdfIN():
    #Function to upload a file
    if not request.json or not 'name' in request.json:
        return(wrong_input())
    new_File1 = { 'name' : request.json.get('name', "") }
    srdFList.append(new_File1)
    return jsonify({'flist': srdFList})


@srdfile.route('/flist/<DFNAME>', methods = [ 'DELETE' ] )
def srdfDEL(DFNAME):
    #Function to delete a given filename
    del_File1 = [ delFile for delFile in srdFList if delFile['name'] == DFNAME ]
    if len(del_File1) == 0:
        return(wrong_del(DFNAME))
    srdFList.remove(del_File1[0])
    return jsonify({'RESULT': True})


if __name__ == "__main__":
    srdfile.run(host='0.0.0.0',port=8080,debug=True)

