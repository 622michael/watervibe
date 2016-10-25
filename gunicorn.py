import "multiprocessing"

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu() + 1
access_logfile = "logs/gunicorn_access.log"
error-logfile = "logs/gunicorn_error.log"
capture-output = True
