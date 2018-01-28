# SFTP REST Browser

This software is a simple service allowing browsing a remote SFTP server through
a simple REST interface.

## Warning

* There is no security configured or offered by the tool. Please protect it with
  whatever measures you deem necessary (HTTP auth, TLS mutual, etc) to avoid any
  kind of unauthorized access to your data while using this software.

## Usage

The remote SFTP server will be accessed through normal HTTP paths. For example,
in order to see the contents of the directory 'in' in the remote server, the
following interaction would take place:

```ShellSession
$ curl http://127.0.0.1:5000/in/
[
  {
    "atime": "2018-01-28 21:34:02", 
    "gid": 121, 
    "mode": "644", 
    "mtime": "2018-01-28 20:03:49", 
    "name": "dhcpd.conf", 
    "resource": "http://127.0.0.1:5000/in/dhcpd.conf", 
    "size": 298, 
    "type": "file", 
    "uid": 1001
  }, 
  {
    "atime": "2018-01-28 21:36:23", 
    "gid": 0, 
    "mode": "755", 
    "mtime": "2018-01-28 21:36:11", 
    "name": "test", 
    "resource": "http://127.0.0.1:5000/in/test", 
    "size": 3, 
    "type": "file", 
    "uid": 0
  }
]

```

When a *directory* is accessed through the tool through a normal *HTTP PATH*,
a simple JSON representation of a list will be returned. This list contains JSON
objects representing the files found in the remote directory targeted through
the HTTP path, as below:

```json
[
  {
    "atime": "2018-01-28 21:34:02",
    "gid": 121,
    "mode": "644",
    "mtime": "2018-01-28 20:03:49",
    "name": "dhcpd.conf",
    "resource": "http://127.0.0.1:5000/in/dhcpd.conf",
    "size": 298,
    "type": "file",
    "uid": 1001
  },
  {
    "atime": "2018-01-28 21:36:23",
    "gid": 0,
    "mode": "755",
    "mtime": "2018-01-28 21:36:11",
    "name": "test",
    "resource": "http://127.0.0.1:5000/in/test",
    "size": 3,
    "type": "file",
    "uid": 0
  }
]
```

The following fields will be available for each object:

* name: file or directory name
* uid: numeric UID of the remote owner
* gid: numerid GID of the remote owner
* mode: UNIX access mode (octal)
* size: size in bytes
* atime: last access time in human readable format
* mtime: last modification time in human readable format
* resource: URL to reach the resource in the file browser

In case the object accessed is a file, the content will be displayed in the
browser.

If the path does not exist in the remote server, a *404* response will be
returned together with a helpful error message:

```json
{
  "message": "the path 'in/inexistent' does not exist in the remote server"
}
```

## Configuration

The following environment variables are *mandatory* for the service to
start:

* SFTP_REST_REMOTE_USER_KEY: path of the SSH key for the the user
* SFTP_REST_REMOTE_USER: name of the user in the remote server
* SFTP_REST_REMOTE_HOST: IP or hostname of the remote server

The following variables are *optional*. If they are not specified, the service
will start with default values:

* SFTP_REST_BIND_HOST: host to which the application will bind. Defaults to
  '127.0.0.1'.
* SFTP_REST_BIND_PORT: port to which the application will bind. Defaults to
  5000.

## Deployment

It is *mandatory* to load the SSH host fingerprint of the remote host into the
hosts file of the user that will be executing the service. This is not handled
by the service itself.

A systemd service file is provided as a deployment suggestion for the service.

## License

MIT License
