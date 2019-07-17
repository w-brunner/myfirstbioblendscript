from bioblend import galaxy
from bioblend.galaxy.objects import *
import bioblend
import sys # for taking arguements
from optparse import OptionParser # for taking options;

args=None

parser = OptionParser()

parser.add_option('--localkey', dest="localkey")
#parser.add_option('--remotekey', dest="remotekey")
options, args = parser.parse_args(args)

gi_local = galaxy.GalaxyInstance(url = "http://localhost:8080", key = options.localkey) # gi_local = galaxy instance; requires an API key to "log in" via code
#gi_remote = galaxy.GalaxyInstance(url = "", key = options.remotekey)

allusers = gi_local.users.get_users()

# TODO: Unify all these loops...

# Create API keys for users that don't have one
for x in range(0, len(allusers)):
    print("Username: " + allusers[x]['username'])
    if(gi_local.users.get_user_apikey(allusers[x]['id']) == "Not available."):
        gi_local.users.create_user_apikey(allusers[x]['id']) # create API key for users that don't have one
        print("Created User API Key for User " + allusers[x]['username'])
        print("User API Key: " + gi_local.users.get_user_apikey(allusers[x]['id']) + "\n")

    else:
        print("User API Key: " + gi_local.users.get_user_apikey(allusers[x]['id']) + "\n")

# Put all galaxy instances under one dictionary
all_apikeys = []
all_gi_local = []
for i in range(0, len(allusers)):
    all_apikeys.append(gi_local.users.get_user_apikey(allusers[i]['id']))
    all_gi_local.append({'username': allusers[i]['username'],  'id': gi_local.users.get_user_apikey(allusers[i]['id']), 'gi_local': galaxy.GalaxyInstance(url = "http://localhost:8080", key = all_apikeys[i])})

all_workflows = [] # All of the workflows in the enviroment, organized by user
for j in range(0, len(all_gi_local)):
    all_workflows.append({'username': allusers[j]['username'], 'workflows': all_gi_local[j]['gi_local'].workflows.get_workflows()})

workflow_exports = []
# TODO: Find a way to save the assc. username of each workflow
for k in range(0, len(all_workflows)): # User
    for a in range(0, len(all_workflows[k]['workflows'])):#Workflows within users
        workflow_exports.append(gi_local.workflows.export_workflow_dict(all_workflows[k]['workflows'][a]['id']))
        gi_local.workflows.export_workflow_to_local_path(all_workflows[k]['workflows'][a]['id'], '/home/will/Documents/galaxy_bioblend_dev/' + all_workflows[k]['workflows'][a]['owner'] + "_" + all_workflows[k]['workflows'][a]['name'], use_default_filename=False)# Append the workflow name with name of user
        print("Exported " + all_workflows[k]['workflows'][a]['owner'] + "\'s workflow, " + all_workflows[k]['workflows'][a]['name'])
