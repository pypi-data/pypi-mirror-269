# Fossil Director

Fossil-director is an HTTP/SCGI server used to host multiple [Fossil](https://fossil-scm.org) repositories, based on the hostname.

The server is meant to run behind nginx or other reverse proxy. Either HTTP or SCGI can be used, though SCGI is [probably preferable](https://fossil-scm.org/home/doc/trunk/www/server/debian/nginx.md#http). Fossil-director will inspect the incoming HTTP `Host:` header and dispatch to the configured fossil repository.

## Installation

(Requires Python >= 3.8)

`pip install fossil-director`

## Configuration

A configuration `.ini` is required. At minimum, define a hostname and path to the fossil repository:

```ini
[example.com]
repo = /path/to/repo.fossil
```

Each virtual host is a new section. Here are all of the options:
```ini
[foo.org]
repo = /other/path.fossil
repolist = false                  # if repo is a directory, set this to true to serve 
                                  # a directory index of fossil files
baseurl = http://foo.org/fossil/  # base url
args = --nodelay --acme           # extra arguments to the `fossil http` command
```

By default, the server runs on port 7000. Here are the server options:

```ini
[server]
host = 127.0.0.1
port = 7000
scgi = true   # to run as an SCGI server
fossil_cmd = /usr/local/bin/fossil  # path to fossil executable

```

## Running

`fossil-director /path/to/config.ini`

Here's an [example systemd service](/file?name=fossil-director.service)


