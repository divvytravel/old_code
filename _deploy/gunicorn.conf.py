__author__ = 'indieman'

bind = "127.0.0.1:8888"
workers = 1
user = "divvy"
group = "divvy"
logfile = "/srv/sites/divvy/log/gunicorn.log"
loglevel = "info"
proc_name = "divvy"
pidfile = '/srv/sites/divvy/pid/gunicorn_divvy.pid'
