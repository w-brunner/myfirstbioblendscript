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
