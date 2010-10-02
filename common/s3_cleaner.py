#!/usr/bin/python
import os, sys, boto, utils
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import simplejson

if len(sys.argv) != 3:
	print "Usage: %s <desktop|mobile> <branch>" % sys.argv[0]
	sys.exit(1)

(type, branch) = sys.argv[1:]
cfg = utils.get_build_config()
if not cfg.verify_aws():
	print "Error: Need both AWS_KEY and AWS_SECRET in the environment or config.json"
	sys.exit(1)

bucket = cfg.open_bucket()

keys = []
prefix = type+'/'+branch
for key in bucket.list(prefix=prefix):
	if key.name != prefix and key.name != prefix+'/' and key.name != prefix+'/index.json':
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
index_key = bucket.get_key('%s/index.json' % prefix)
if index_key != None:
	index = simplejson.loads(index_key.get_contents_as_string())
	objects_to_remove = []
	for key in deleted_keys:
		for obj in index:
			if key == '%s/%s' % (prefix, obj['filename']):
				objects_to_remove.append(obj)

	print 'removing %d items from index.json...' % len(objects_to_remove)
	for obj in objects_to_remove:
		index.remove(obj)

	index_key.set_contents_from_string(simplejson.dumps(index))
	index_key.make_public()

print "Cleaned %d binaries from S3" % cleaned
