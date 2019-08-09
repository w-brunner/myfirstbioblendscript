from bioblend import galaxy
from bioblend.galaxy.objects import *
import bioblend
import sys # for taking arguements
from optparse import OptionParser # for taking options;

args = None

parser = OptionParser()

parser.add_option('--localkey', dest = "localkey")
parser.add_option('--remotekey', dest = "remotekey")
parser.add_option('--remoteurl', dest = "remoteurl")
parser.add_option('--savedir', dest = "savedir")
options, args = parser.parse_args(args)

gi_local = galaxy.GalaxyInstance(url = "http://localhost:8080", key = options.localkey) # gi_local = galaxy instance; requires an API key to "log in" via code
gi_remote = galaxy.GalaxyInstance(url = options.remoteurl, key = options.remotekey)

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
    all_gi_local.append({'username': allusers[i]['username'], 'id': gi_local.users.get_user_apikey(allusers[i]['id']),
    'gi_local': galaxy.GalaxyInstance(url = "http://localhost:8080", key = all_apikeys[i])})

all_workflows = [] # All of the workflows in the enviroment, organized by user
for j in range(0, len(all_gi_local)):
    all_workflows.append({'username': allusers[j]['username'], 'workflows': all_gi_local[j]['gi_local'].workflows.get_workflows()})

workflow_exports = [] # All of the workflows of the galaxy enviroment
savedworkflow_names = [] # The ordered names of each workflow being exported
for k in range(0, len(all_workflows)): # User
    for a in range(0, len(all_workflows[k]['workflows'])):#Workflows within users
        all_workflows[k]['workflows'][a]['name'] = all_workflows[k]['username'] + "_" + all_workflows[k]['workflows'][a]['name']
        workflow_exports.append(gi_local.workflows.export_workflow_dict(all_workflows[k]['workflows'][a]['id']))
        """gi_local.workflows.export_workflow_to_local_path(all_workflows[k]['workflows'][a]['id'],
        options.savedir + all_workflows[k]['workflows'][a]['name'] + ".ga",
        use_default_filename=False)""" # I can't export to disk b/c the names aren't exported, and thus the names need to be changed post-export
        savedworkflow_names.append(all_workflows[k]['workflows'][a]['name'])
        print("Exported " + all_workflows[k]['workflows'][a]['owner'] + "\'s workflow, " + all_workflows[k]['workflows'][a]['name'])

for l in range(0, len(savedworkflow_names)):
    #gi_remote.workflows.import_workflow_from_local_path(options.savedir + savedworkflow_names[l] + ".ga")
    print("Uploaded workflow " + options.savedir + savedworkflow_names[l] + ".ga")
    workflow_exports[l]['name'] = savedworkflow_names[l]
    gi_remote.workflows.import_workflow_dict(workflow_exports[l])
    #pass

#alltools = gi_local.tools.get_tools() + gi_remote.tools.get_tools()
#toolslist_unique = []

#for tool in alltools:
#    if tool['id'] not in toolslist_unique:
#        toolslist_unique.append(tool['id'])
#    else:
#        pass

workflow_tools = []


for workflow in workflow_exports:
    for step in workflow['steps']:
        if workflow['steps'][step]['tool_id'] is None:
            pass
        else:
            workflow_tools.append(workflow['steps'][step]['tool_id'])

workflow_tools = list(set(workflow_tools))
remote_tools_list = gi_remote.tools.get_tools()
remote_tools_list_ids = []
missing_tools_remote = []

for tool in remote_tools_list:
    remote_tools_list_ids.append(tool['id'])

for tool in workflow_tools:
    if tool not in remote_tools_list_ids:
        missing_tools_remote.append(tool)# Tool is missing from remote!
        
print(missing_tools_remote) # *DING!*
