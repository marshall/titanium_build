#!/usr/bin/python
import sys, os
from boto.s3.connection import S3Connection
from boto.s3.key import Key

if len(sys.argv) != 7:
	print "Usage: %s <AWS Access Key> <AWS Secret Key> <desktop|mobile> <path> <revision> <build url>" % sys.argv[0]
	sys.exit(1)

access_key = sys.argv[1]
secret_key = sys.argv[2]
type = sys.argv[3]
path = sys.argv[4]
revision = sys.argv[5]
build_url = sys.argv[6]

filename = os.path.basename(path)

conn = S3Connection(access_key, secret_key)
bucket = conn.get_bucket('nightlies')
key = Key(bucket)
key.key = '%s/%s' % (type, filename)
key.set_metadata('git_revision', revision)
key.set_metadata('build_url', build_url)
key.set_contents_from_filename(path)
