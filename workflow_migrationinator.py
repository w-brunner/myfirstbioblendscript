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
parser.add_option('--remotekey', dest = "remotekey")
parser.add_option('--remoteurl', dest = "remoteurl")
parser.add_option('--savedir', dest = "savedir")
options, args = parser.parse_args(args)

gi_local = galaxy.GalaxyInstance(url = "http://localhost:8080", key = options.localkey) # gi_local = galaxy instance; requires an API key to "log in" via code
gi_remote = galaxy.GalaxyInstance(url = options.remoteurl, key = options.remotekey)

all_workflow_dicts = gi_local.workflows.get_workflows()
all_users_dicts = gi_local.users.get_users()

workflows_tools = []

for user in all_users_dicts:# Galaxy instances need to be initiated 
    #check for API key first!
    if gi_remote.users.get_user_apikey(user['id']) == "Not available.":
        apikey = gi_remote.users.create_user_apikey(user['id'])
    else
        apikey = gi_remote.users.get_user_apikey(user['id'])
    current_gi = (galaxy.GalaxyInstance(url = options.remotekey, apikey))
    #Export the workflows into a list of dictionaries
    workflows_dicts = current_gi.workflows.get_workflows()
    workflow_exports = []
    for workflow_dict in workflows_dicts:
        workflow_exports.append(current_gi.workflows.export_workflow_dict(workflow_dict['id']))
        
    for workflow_export in workflows_exports: # Find the tool IDs of all tools used by the user
        for step in workflow_export['steps']:
            workflows_tools.append(step['tool_id'])

instance_tools = gi_remote.tools.get_tools()
tool_ids = []

for tool in instance_tools:
    tool_ids.append(tool['id'])
