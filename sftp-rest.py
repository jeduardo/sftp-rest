#!/usr/bin/env python3

""" A REST browser for SFTP servers """

import pysftp
import os
import sys
import tempfile

from datetime import datetime
from flask import Flask
from flask import jsonify, make_response, request, send_file


# Retrieving application configuration
remote_host = os.environ.get('SFTP_REST_REMOTE_HOST', None)
remote_user = os.environ.get('SFTP_REST_REMOTE_USER', None)
key = os.environ.get('SFTP_REST_REMOTE_USER_KEY', None)
host = os.environ.get('SFTP_REST_BIND_HOST', '127.0.0.1')
port = os.environ.get('SFTP_REST_BIND_PORT', 5000)

# Starting app only if application is configured
if not remote_host or not remote_user or not key:
    print('Configuration is missing one item, application will not start')
    sys.exit(1)

app = Flask(__name__)


@app.route('/', defaults={'path': '/'}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def list(path):
    """ Return a JSON representation of a list of files for directories and the
    file content for actual files """
    sftp = pysftp.Connection(remote_host, username=remote_user,
                             private_key=key)
    try:
        if sftp.isdir(path):
            files = []
            root = request.url
            if not root.endswith('/'):
                root = root + '/'
            for attr in sftp.listdir_attr(path):
                if sftp.isdir(attr.filename):
                    t = 'dir'
                else:
                    t = 'file'
                obj = {
                    'resource': root + attr.filename,
                    'name': attr.filename,
                    'size': attr.st_size,
                    'uid': attr.st_uid,
                    'gid': attr.st_gid,
                    'mode': str(oct(attr.st_mode))[-3:],
                    'atime': str(datetime.fromtimestamp(attr.st_atime)),
                    'mtime': str(datetime.fromtimestamp(attr.st_mtime)),
                    'type': t,
                }
                files.append(obj)
            return jsonify(files)
        else:
            f = open(tempfile.mktemp(), 'w')
            try:
                sftp.get(path, localpath=f.name, preserve_mtime=True)
                return send_file(f.name)
            finally:
                os.remove(f.name)
    except FileNotFoundError:
        error = {
            'message': 'the path \'%s\' does not exist in the remote server' %
            path,
        }
        return make_response(jsonify(error), 404)


if __name__ == '__main__':
    app.run(host=host, port=port)
