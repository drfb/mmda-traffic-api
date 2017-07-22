import os


HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '8000'))
DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'

MMDA_API_URL = os.getenv('MMDA_API_URL')
