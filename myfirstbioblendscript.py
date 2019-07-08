from bioblend import galaxy
from bioblend.galaxy.objects import *
import bioblend
import sys # for taking arguements
from optparse import OptionParser # for taking options;

args=None

parser = OptionParser()

parser.add_option('--apikey', dest="argkey")
options, args = parser.parse_args(args)

gi = galaxy.GalaxyInstance(url = "http://localhost:8080", key = options.argkey) # gi = galaxy instance; requires an API key to "log in" via code

allusers = gi.users.get_users()

for x in range(0, len(allusers)):
    print(allusers[x]['username'])
