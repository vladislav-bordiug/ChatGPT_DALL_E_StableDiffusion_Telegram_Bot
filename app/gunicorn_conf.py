import multiprocessing
import os

workers = multiprocessing.cpu_count() * 2 + 1

port = int(os.environ.get("PORT", "5000"))
bind = f"0.0.0.0:{port}"
worker_class = "uvicorn.workers.UvicornWorker"
loglevel = "info"