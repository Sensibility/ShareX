import sys
from os.path import dirname, abspath

sys.path.insert(0, abspath(dirname(sys.argv[0])))

from main import flaskApp