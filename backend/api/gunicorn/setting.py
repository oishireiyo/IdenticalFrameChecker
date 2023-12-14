import os

wsgi_app = 'server:app'
chdir = '/backend/api'
reload = False
accesslog = '-'
errorlog = '-'
loglevel = 'info'
proc_name = 'TimeCode-backend-gunicorn'
bind = '0.0.0.0:' + os.getenv('EXPOSED_PORT', 5432)
workers = 1