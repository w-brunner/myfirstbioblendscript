from bioblend import galaxy
from bioblend.galaxy.objects import *
import bioblend
import sys # for taking arguements
from optparse import OptionParser # for taking options;

args = None

parser = OptionParser()

parser.add_option('--remotekey', dest = "remotekey")
parser.add_option('--remoteurl', dest = "remoteurl")
parser.add_option('--filter', dest = "filterkey")

options, args = parser.parse_args(args)

gi_remote = galaxy.GalaxyInstance(url = options.remoteurl, key = options.remotekey)

all_workflows = gi_remote.workflows.get_workflows()

for x in range(len(all_workflows)):
    if filterkey in all_workflows[x]['name']:
        gi_remote.workflows.delete_workflow(all_workflows[x]['id'])
        print("Deleting workflow " + all_workflows[x]['name'])
