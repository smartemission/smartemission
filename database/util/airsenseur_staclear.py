#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import sys, requests


def sta_rest(url, method, user=None, password=None):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    print('START Request: %s %s' % (method, url))

    if method == 'GET':
        # Use requests module to send a GET request
        response = requests.get(url, headers=headers)
    elif method == 'DELETE':
        # Use requests module to send a DELETE request
        response = requests.delete(url, headers=headers, auth=(user, password))
    else:
        print("Unknown method: " + method)
        sys.exit(-1)

    print('Status: %d' % response.status_code)
    print('Response: %s' % response.text)

    print('END Request: %s %s\n' % (method, url))
    return response


def delete_ase_things(url, user, password):
    get_url = url + 'Things?$filter=properties/project_id%20eq%20%271182%27'

    ase_things = sta_rest(get_url, 'GET').json()
    for thing in ase_things['value']:
        sta_rest(url + '%s(%d)' % ('Things', thing['@iot.id']), 'DELETE', user, password)

if __name__ == '__main__':
    url = sys.argv[1]
    user = sys.argv[2]
    password = sys.argv[3]

    # Delete all ASE Things
    delete_ase_things(url, user, password)  # also deletes Datastreams and Observations
