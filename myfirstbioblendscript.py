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

# Create API keys for users that don't have one
for x in range(0, len(allusers)):
    print(allusers[x]['username'])
    if(gi.users.get_user_apikey(allusers[x]['id']) == "Not available."):
        gi.users.create_user_apikey(allusers[x]['id']) # create API key for users that don't have one
        print(gi.users.get_user_apikey(allusers[x]['id']))
    else:
        print(gi.users.get_user_apikey(allusers[x]['id']))
