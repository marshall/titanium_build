#!/usr/bin/env python
import sys, os
build_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
common_dir = os.path.join(build_dir, 'common')
sys.path.append(common_dir)

import utils
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import simplejson

def usage():
	print "Usage: %s (add|remove|list) (mobile|desktop) <branch>"
	sys.exit(1)

if len(sys.argv) < 3: usage()

command = sys.argv[1]
type = sys.argv[2]
if command in ['add', 'remove']:
	if len(sys.argv) != 4:
		usage()
	branch = sys.argv[3]
	
cfg = utils.get_build_config()
if not cfg.verify_aws():
	print "Error: Need both AWS_KEY and AWS_SECRET in the environment or config.json"
	sys.exit(1)

bucket = cfg.open_bucket()
branches_key = '%s/branches.json' % type
branches = utils.get_key_json_array(bucket, branches_key)

def list_branches():
	print 'Branches for %s:' % type
	for branch in branches:
		print '  %s' % branch
if command == 'list':
	list_branches()
elif command == 'add':
	if branch in branches:
		print 'Error: branch %s already in branch list, ignoring' % branch
		sys.exit(1)
	branches.append(branch)
	utils.set_key_json_array(bucket, branches_key, branches)
	list_branches()
elif command == 'remove':
	if not branch in branches:
		print 'Error: branch %s isn\'t currently in branch list, ignoring' % branch
		sys.exit(1)
	branches.remove(branch)
	utils.set_key_json_array(bucket, branches_key, branches)
	list_branches()
