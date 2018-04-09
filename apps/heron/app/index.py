import os, sys
import requests
import logging
from functools import wraps, update_wrapper
from urlparse import urlparse
from datetime import datetime
from flask import Flask, Response, render_template, request, make_response, stream_with_context
from werkzeug.utils import secure_filename
from reverseproxied import ReverseProxied
from config import config

if __name__ != '__main__':
    # When run with WSGI in Apache we need to extend the PYTHONPATH to find Python modules relative to index.py
    sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)
app.debug = True
UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')

log = logging.getLogger(__name__)
log.setLevel(config['loglevel'])

CHUNK_SIZE = 1024

# Wrapper to disable any kind of caching for all pages
# See http://arusahni.net/blog/2014/03/flask-nocache.html
def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


def access_denied():
    return Response("{'access':'denied'}", status=403, mimetype='application/json')

def url2toplevel_domain(url):
    referer_host_port = urlparse(url).netloc
    # Extract top-level domain
    return '.'.join(referer_host_port.split(':')[0].split('.')[-2:])

# Home page
@app.route('/')
@nocache
def home():
    return render_template('index.html')


@app.route('/cgi-bin/proxy.cgi', methods=['GET', 'POST'])
@nocache
def proxy():
    if 'referer' not in request.headers:
        return access_denied()
    else:
        allowed_referers = config['proxy_referers']

        # Extract top-level domain
        referer_domain = url2toplevel_domain(request.headers['referer'])
        log.debug('referer_domain=%s' % referer_domain)
        if referer_domain not in allowed_referers:
            log.warn('access denied: referer_domain=%s' % referer_domain)
            return access_denied()

    url = request.args.get('url')

    # Rule out alt protocol requests
    if not url.startswith('http'):
        log.warn('access denied: url=%s' % url)
        return access_denied()

    # Check hosts
    allowed_hosts = config['proxy_hosts']
    if allowed_hosts and allowed_hosts is not '*':
        # Extract top-level domain
        host_domain = url2toplevel_domain(url)
        if host_domain not in allowed_hosts:
            log.warn('access denied, for host=%s url=%s' % (host_domain, url))
            return access_denied()

    request_headers = {}
    if request.method == "POST":
        data = request.data
        request_headers["Content-Length"] = str(len(data))
        request_headers['Content-Type'] = request.headers['content-type']
        req = requests.post(url, headers=request_headers, data=data)
        content = req.content
        return content, {'Content-Type': req.headers['content-type']}
    else:

        def generate():
            for chunk in req.iter_content(CHUNK_SIZE):
                yield chunk

        req = requests.get(url, stream=True, params=request.args, headers={})
        # req = requests.get(url, stream=True)
        return Response(generate(), content_type=req.headers['content-type'])


@app.route('/cgi-bin/heron.cgi', methods=['GET', 'POST'])
@nocache
def heron():
    from heron import handler
    if request.method == "POST":
        params = dict()
        for param_name in request.form:
            params[param_name] = request.form[param_name]

        # check if the post request has the file part
        if 'file' in request.files:
            f = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if f.filename == '':
                return 'no file supplied'
            file = dict()
            file['filename'] = secure_filename(f.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            file['value'] = f.read()
            params['file'] = file
            
    else:
        params = request.args

    status, response_headers, data = handler(params)
    return data, response_headers
    # return Response()


if __name__ == '__main__':
    # Run as main via python index.py
    app.run(debug=True, host='0.0.0.0')


