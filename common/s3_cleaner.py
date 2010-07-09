#!/usr/bin/python
import os, sys, boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import simplejson

if len(sys.argv) != 4:
	print "Usage: %s <AWS Access Key> <AWS Secret Key> <desktop|mobile>" % sys.argv[0]
	sys.exit(1)

access_key = sys.argv[1]
secret_key = sys.argv[2]
type = sys.argv[3]

conn = S3Connection(access_key, secret_key)
bucket = conn.get_bucket('builds.appcelerator.com')

keys = []
for key in bucket.list(prefix=type):
	if key.name != type and key.name != type+'/' and key.name != type+'/index.json':
		keys.append(key)

cleaned = 0
deleted_keys = []
if (len(keys) > 15):
	# only keep the last 5 builds * 3 platforms = 15 files
	keys.sort(lambda a,b: cmp(a.last_modified, b.last_modified))
	for i in range(0, len(keys)-15):
		key = keys[i]
		print 'deleting ' + str(keys[i])
		deleted_keys.append(key.name)
		key.delete()
		cleaned += 1

# maintain the index JSON
index_key = bucket.get_key('%s/index.json' % type)
if index_key != None:
	print 'removing %d items from index.json...' % cleaned
	index = simplejson.loads(index_key.get_contents_as_string())
	objects_to_remove = []
	for key in deleted_keys:
		for obj in index:
			if key == '%s/%s' % (type, obj['filename']):
				indexes_to_remove.append(obj)

	for obj in objects_to_remove:
		index.remove(obj)

	index_key.set_contents_from_string(simplejson.dumps(index))
	index_key.make_public()

print "Cleaned %d binaries from S3" % cleaned
