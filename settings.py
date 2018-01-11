import os

ADMIN_PHONE = '12345678'

HOST = '0.0.0.0'
PORT = 5000

SECRET_KEY = ''

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'base.db')
PIE = os.path.join(PROJECT_ROOT, 'static')
