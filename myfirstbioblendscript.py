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

# TODO: Unify all these loops...

# Create API keys for users that don't have one
for x in range(0, len(allusers)):
    print("Username: " + allusers[x]['username'])
    if(gi.users.get_user_apikey(allusers[x]['id']) == "Not available."):
        gi.users.create_user_apikey(allusers[x]['id']) # create API key for users that don't have one
        print("User API Key: " + gi.users.get_user_apikey(allusers[x]['id']))

    else:
        print("User API Key: " + gi.users.get_user_apikey(allusers[x]['id']))

# Put all galaxy instances under one dictionary
all_apikeys = []
all_gi = []
for i in range(0, len(allusers)):
    all_apikeys.append(gi.users.get_user_apikey(allusers[i]['id']))
    all_gi.append({'username': allusers[i]['username'],  'id': gi.users.get_user_apikey(allusers[i]['id']), 'gi': galaxy.GalaxyInstance(url = "http://localhost:8080", key = all_apikeys[i])})
print(gi.workflows.get_workflows())

all_workflows = [] # All of the workflows in the enviroment, organized by user
for j in range(0, len(all_gi)):
    all_workflows.append({'username': allusers[j]['username'], 'workflows': all_gi[j]['gi'].workflows.get_workflows()})

workflow_exports = []
for k in range(0, len(all_workflows)):
    for a in range(0, len(all_workflows[k])):
        workflow_exports.append(gi.workflows.export_workflow_dict(all_workflows[a]['workflows'][0]['id']))
