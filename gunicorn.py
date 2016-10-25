import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() + 1
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
capture_output = True
