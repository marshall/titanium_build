#!/usr/bin/python
import os, sys, boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key

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
	if key.name != type:
		keys.append(key)

cleaned = 0
if (len(keys) > 15):
	# only keep the last 5 builds * 3 platforms = 15 files
	keys.sort(lambda a,b: cmp(a.last_modified, b.last_modified))
	for i in range(15, len(keys)):
		key = keys[i]
		key.delete()
		cleaned += 1

print "Cleaned %d binaries from S3" % cleaned
