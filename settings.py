import os

DEBUG = True
PORT = 8080
SECRET_KEY = os.urandom(16)
WTF_CSRF_ENABLED = True