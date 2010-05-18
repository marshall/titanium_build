#!/usr/bin/python
import sys, os
from boto.s3.connection import S3Connection
from boto.s3.key import Key

if len(sys.argv) != 5:
	print "Usage: %s <AWS Access Key> <AWS Secret Key> <desktop|mobile> <path>" % sys.argv[0]
	sys.exit(1)

access_key = sys.argv[1]
secret_key = sys.argv[2]
type = sys.argv[3]
path = sys.argv[4]

filename = os.path.basename(path)

conn = S3Connection(access_key, secret_key)
bucket = conn.get_bucket('nightlies')
key = Key(bucket)
key.key = '%s/%s' % (type, filename)
key.set_contents_from_filename(path)
