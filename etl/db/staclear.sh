#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os, sys, requests, json

def callWebserviceDelete(entity):
  url = "http://scratchpad.sensorup.com/OGCSensorThings/v1.0/"+entity
  headers ={"Content-Type": "application/json", "Accept": "application/json"}

  # Use requests module to send a DELETE request
  request = requests.delete(url, headers = headers)

  # print the status code
  print(request.status_code)  # status-code should be 201, to let us know the entity has been created

  if request.status_code != 200:
    #print error, do something
    print("Error")
  else:
    #print success, do something
    print("Success")

if __name__ == '__main__':
  # Call method in order to perform a DELETE request to the webservice
  callWebserviceDelete("Things(29761)")
