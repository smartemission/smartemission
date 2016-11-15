#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import sys, requests


def sta_rest(url, method, user=None, password=None):
  headers ={"Content-Type": "application/json", "Accept": "application/json"}

  print('START Request: %s %s' % (method, url))

  if method == 'GET':
    # Use requests module to send a GET request
    response = requests.get(url, headers = headers)
  elif method == 'DELETE':
    # Use requests module to send a DELETE request
    response = requests.delete(url, headers = headers, auth=(user, password))
  else:
    print("Unknown method: " + method)
    sys.exit(-1)

  print('Status: %d' % response.status_code)
  print('Response: %s' % response.text)

  print('END Request: %s %s\n' % (method, url))
  return response


def delete_entities(url, entity_name, user, password):
  entities = sta_rest(url + entity_name, 'GET').json()
  for entity in entities['value']:
    sta_rest(url + '%s(%d)' % (entity_name, entity['@iot.id']), 'DELETE', user, password)


if __name__ == '__main__':
  host = sys.argv[1]
  port = sys.argv[2]
  user = sys.argv[3]
  password = sys.argv[4]

  url = "http://%s:%s/OGCSensorThings/v1.0/" % (host, port)

  # Delete all entities
  delete_entities(url, 'Things', user, password) # also deletes Datastreams and Observations
  delete_entities(url, 'Locations', user, password)
  delete_entities(url, 'Sensors', user, password)
  delete_entities(url, 'ObservedProperties', user, password)
  delete_entities(url, 'FeaturesOfInterest', user, password)
