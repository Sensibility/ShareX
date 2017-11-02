import sys, os

sys.path.insert(0, '/var/www/ShareX')
os.chdir('ShareX')

from main import flaskApp as application