#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask


import flask
from flask import Flask, request
import json
app = Flask(__name__)
app.debug = True

# An example world
# {
#    'a':{'x':1, 'y':2},
#    'b':{'x':2, 'y':3}
# }

class World:
    def __init__(self):
        self.clear()
        
    # What is entity, key, value?    
    # I think this changes an EXISTING entity
    def update(self, entity, key, value):
        entry = self.space.get(entity,dict())
        entry[key] = value
        self.space[entity] = entry

    # I think this creates a NEW entity. Or it completely overwrites it
    def set(self, entity, data):
        self.space[entity] = data

    # I think this DELETES all entities because space is the dict containing all entities. It is cleared here.
    def clear(self):
        self.space = dict()

    def get(self, entity):
        return self.space.get(entity,dict())
    
    def world(self):
        return self.space

# you can test your webservice from the commandline
# curl -v -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}' 

myWorld = World()

# I give this to you, this is how you get the raw body/data portion of a post in flask
# this should come with flask but whatever, it's not my project.
def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data.decode("utf8") != u''):
        return json.loads(request.data.decode("utf8"))
    else:
        return json.loads(request.form.keys()[0])

@app.route("/")
def hello():
    '''Return something coherent here.. perhaps redirect to /static/index.html '''
    
    # I don't think the world should be return here?
    return flask.redirect("/static/index.html")

# curl -v -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}' 
# curl -v -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}'
@app.route("/entity/<entity>", methods=['POST','PUT'])
def update(entity):
    '''update the entities via this interface'''

    requestData = flask_post_json()

    # get the <entity> url param from the entity variable
    myEntity = myWorld.get(entity)

    # If an entity doesn't exist, create a new one
    if myEntity == {}:
        myWorld.set(entity, requestData)
    else:
        for key in requestData.keys():
            # print("Key:", key, "Value:", requestData[key])
            myWorld.update(entity, key, requestData[key])

    return (json.dumps(requestData), 200)

# curl -v -H "Content-Type: application/json" -X GET http://127.0.0.1:5000/world
@app.route("/world", methods=['POST','GET'])    
def world():
    '''you should probably return the world here'''

    return (json.dumps(myWorld.world()), 200)

# curl -v -H "Content-Type: application/json" -X GET http://127.0.0.1:5000/entity/X
@app.route("/entity/<entity>")    
def get_entity(entity):
    '''This is the GET version of the entity interface, return a representation of the entity'''

    return (json.dumps(myWorld.get(entity)), 200)

# curl -v -H "Content-Type: application/json" -X GET http://127.0.0.1:5000/clear -d
# curl -v -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/clear -d
@app.route("/clear", methods=['POST','GET'])
def clear():
    '''Clear the world out!'''
    
    myWorld.clear()
    
    # use 204
    return (json.dumps({}), 200)

if __name__ == "__main__":
    app.run()