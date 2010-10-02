#!/usr/bin/env python
# prints the value of a pseudo-JS expression against the build index ("index" is the variable name)

import sys, os
build_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
common_dir = os.path.join(build_dir, 'common')
sys.path.append(common_dir)

import utils
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import simplejson

if len(sys.argv) < 3:
	print "Usage: %s (mobile|desktop) <branch> (expression?)" % sys.argv[0]
	sys.exit(1)

type = sys.argv[1]
branch = sys.argv[2]
expression = None
if len(sys.argv) > 3:
	expression = sys.argv[3]

cfg = utils.get_build_config()
if not cfg.verify_aws():
	print "Error: Need both AWS_KEY and AWS_SECRET in the environment or config.json"
	sys.exit(1)

class JSONObject(object):
	def __init__(self, json):
		self.__dict__['json'] = json

	def __getattr__(self, name):
		return JSONObject(self.__dict__['json'][name])

	def __setattr__(self, name, value):
		self.__dict__['json'][name] = value

	def __getitem__(self, name):
		return JSONObject(self.__dict__['json'][name])

	def __setitem__(self, name, value):
		self.__dict__['json'][name] = value

	def __str__(self):
		return simplejson.dumps(self.__dict__['json'])

bucket = cfg.open_bucket()
index_key = '%s/%s/index.json' % (type, branch)
index = JSONObject(utils.get_key_json_array(bucket, index_key))

if expression == None:
	print str(index)
else:
	result = eval(expression)
	print str(result)
