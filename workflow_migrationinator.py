"""
This is the final version of William Brunner's workflow migration script for Galaxy
"""

from bioblend import galaxy
from bioblend.galaxy.objects import *
import bioblend
import sys # for taking arguements
from optparse import OptionParser # for taking options;

args = None

parser = OptionParser()

parser.add_option('--localkey', dest = "localkey")
parser.add_option('--localurl', dest = "localurl")
parser.add_option('--remotekey', dest = "remotekey")
parser.add_option('--remoteurl', dest = "remoteurl")
parser.add_option('--savedir', dest = "savedir")
parser.add_option('--addunames', dest = "addunames", action = "store_true")
parser.add_option('--users', dest = "users")
users = options.users.split(",")
options, args = parser.parse_args(args)

gi_local = galaxy.GalaxyInstance(url = options.localurl, key = options.localkey) # gi_local = galaxy instance; requires an API key to "log in" via code
gi_remote = galaxy.GalaxyInstance(url = options.remoteurl, key = options.remotekey)

all_workflow_dicts = gi_local.workflows.get_workflows()
all_users_dicts = gi_local.users.get_users()

workflows_tools = []

for i, user in enumerate(all_users_dicts):# Galaxy instances need to be initiated
    if user['username'] in users or len(users) is 0:# If user didn't pass a list of users, then the program will default to exporting all.
        #check for API key first!
        if gi_local.users.get_user_apikey(user['id']) == "Not available.":
            apikey = gi_local.users.create_user_apikey(user['id'])
        else:
            apikey = gi_local.users.get_user_apikey(user['id'])
        current_gi = galaxy.GalaxyInstance(url = options.localurl, key = apikey)
        #Export the workflows into a list of dictionaries
        workflows_dicts = current_gi.workflows.get_workflows()
        for workflow_dict in workflows_dicts:
            workflow = current_gi.workflows.export_workflow_dict(workflow_dict['id'])
            if options.addunames:
                workflow['name'] = user['username'] + "_" + workflow['name']
            #TODO Export workflows to remote instance, and export to local file
            gi_remote.workflows.import_workflow_dict(workflow)
            gi_local.workflows.export_workflow_to_local_path(workflow_dict['id'], options.savedir + workflow['name'] + ".ga", use_default_filename=False)
            for step in workflow['steps']: # Find the tool IDs of all tools used by the user
                workflows_tools.append(workflow['steps'][step]["tool_id"])
            print("Finished processing " + workflow['name'])

instance_tools = gi_remote.tools.get_tools()
tool_ids = []

for tool in instance_tools:
    tool_ids.append(tool['id'])

tool_ids = list(set(tool_ids + workflows_tools))

print(tool_ids)
