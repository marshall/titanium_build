#!/usr/bin/env python
import sys, os
build_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
common_dir = os.path.join(build_dir, 'common')
sys.path.append(common_dir)

import utils
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import simplejson

cfg = utils.get_build_config()
if not cfg.verify_aws():
	print "Error: Need both AWS_KEY and AWS_SECRET in the environment or config.json"
	sys.exit(1)

print 'publishing changes to builds.appcelerator.com s3 site...'
bucket = cfg.open_bucket()

web_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), 'web')
for root, dirs, files in os.walk(web_dir):
	rel_path = root[len(web_dir)+1:].replace("\\", '/')
	for file in files:
		full_path = os.path.join(root, file)
		if len(rel_path) > 0:
			key_path = '/'.join([rel_path, file])
		else:
			key_path = file

		key = Key(bucket)
		key.key = key_path
		print 'uploading %s...' % key_path
		key.set_contents_from_filename(full_path)
		key.make_public()
