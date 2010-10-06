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
	print "Usage: %s (add|remove|list|default) (mobile|desktop) <branch>" % sys.argv[0]
	sys.exit(1)

if len(sys.argv) < 3: usage()

command = sys.argv[1]
type = sys.argv[2]
if command in ['add', 'remove', 'default']:
	if len(sys.argv) != 4:
		usage()
	branch = sys.argv[3]
	
cfg = utils.get_build_config()
if not cfg.verify_aws():
	print "Error: Need both AWS_KEY and AWS_SECRET in the environment or config.json"
	sys.exit(1)

bucket = cfg.open_bucket()
branches_key = '%s/branches.json' % type
branches = utils.get_key_json_object(bucket, branches_key)

def list_branches():
	if not 'branches' in branches:
		print 'No branches for %s' % type
		sys.exit(1)
	
	print 'Building branches for %s:' % type
	for branch in branches['branches']:
		if 'defaultBranch' in branches and branches['defaultBranch'] == branch:
			print ' *%s (default)' % branch
		else:
			print '  %s' % branch

def check_branch_exists():
	if not 'branches' in branches or not branch in branches['branches']:	
		print 'Error: branch %s isn\'t currently in the %s branch list' % (branch, type)
		list_branches()
		sys.exit(1)
	
if command == 'list':
	list_branches()

elif command == 'add':
	if 'branches' in branches and branch in branches['branches']:
		print 'Error: branch %s already in branch list, ignoring' % branch
		sys.exit(1)
	if not 'branches' in branches:
		branches['branches'] = []
	branches['branches'].append(branch)
	utils.set_key_json_object(bucket, branches_key, branches)
	list_branches()

elif command == 'remove':
	check_branch_exists()
	if branch == branches['defaultBranch']:
		print 'Error: %s is the current default branch, change it before removing' % branch
		sys.exit(1)
	branches['branches'].remove(branch)
	utils.set_key_json_object(bucket, branches_key, branches)
	list_branches()

elif command == 'default':
	check_branch_exists()
	branches['defaultBranch'] = branch
	utils.set_key_json_object(bucket, branches_key, branches)
	list_branches()
