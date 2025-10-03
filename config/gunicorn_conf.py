import multiprocessing


bind = "0.0.0.0:8000"
workers = 4
worker_class = "gthread"
threads = 2
preload_app = True
timeout = 30
graceful_timeout = 30
keepalive = 5