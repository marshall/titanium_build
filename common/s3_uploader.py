#!/usr/bin/python
import sys, os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import simplejson

if len(sys.argv) != 8:
	print "Usage: %s <AWS Access Key> <AWS Secret Key> <desktop|mobile> <path> <revision> <build url> <sha1>" % sys.argv[0]
	sys.exit(1)

access_key = sys.argv[1]
secret_key = sys.argv[2]
type = sys.argv[3]
path = sys.argv[4]
revision = sys.argv[5]
build_url = sys.argv[6]
sha1 = sys.argv[7]

filename = os.path.basename(path)

print 'uploading %s...' % filename
conn = S3Connection(access_key, secret_key)
bucket = conn.get_bucket('builds.appcelerator.com')
key = Key(bucket)
key.key = '%s/%s' % (type, filename)
key.set_metadata('git_revision', revision)
key.set_metadata('build_url', build_url)
key.set_metadata('build_type', type)
key.set_metadata('sha1', sha1)
key.set_contents_from_filename(path)
key.make_public()

print 'updating %s/index.json..' % type
index_key = bucket.get_key('%s/index.json' % type)
index = []
if index_key == None:
	index_key = Key(bucket)
	key.key = '%s/index.json' % type
else:
	index = simplejson.loads(index_key.get_contents_as_string())

index.append({ 'filename': filename, 'git_revision': revision, 'build_url': build_url, 'build_type': type, 'sha1': sha1 })
index_key.set_contents_from_string(simplejson.dumps(index))
index_key.make_public()
