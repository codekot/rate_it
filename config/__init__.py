from config.config import DATABASE_CONNECTION
try:
    from config.config import DEBUG, HOST, PORT
except:
    DEBUG = HOST = PORT = None
    
