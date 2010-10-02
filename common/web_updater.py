#!/usr/bin/env python

import sys, os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import simplejson

if len(sys.argv) != 3:
	print "Usage: %s <AWS Access Key> <AWS Secret Key>" % sys.argv[0]
	sys.exit(1)

access_key = sys.argv[1]
secret_key = sys.argv[2]

print 'publishing changes to builds.appcelerator.com s3 site...'
conn = S3Connection(access_key, secret_key)
bucket = conn.get_bucket('builds.appcelerator.com')

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
