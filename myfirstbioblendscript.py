from bioblend import galaxy
from bioblend.galaxy.objects import *
import sys # for taking arguements
from optparse import OptionParser # for taking options;

args=None

parser = OptionParser()

parser.add_option('--apikey', dest="argkey")
options, args = parser.parse_args(args)

gi = galaxy.GalaxyInstance(url = "http://localhost:8080", key = options.argkey) # gi = galaxy instance; requires an API key to "log in" via code
