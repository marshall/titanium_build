#!/usr/bin/python
import sys, os, socket, utils
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import simplejson

if len(sys.argv) != 6:
	print "Usage: %s <desktop|mobile> <path> <branch> <revision> <build url>" % sys.argv[0]
	sys.exit(1)

(type, path, branch, revision, build_url) = sys.argv[1:]

cfg = utils.get_build_config()
if not cfg.verify_aws():
	print "Error: Need both AWS_KEY and AWS_SECRET in the environment or config.json"
	sys.exit(1)
	
bucket = cfg.open_bucket()

sha1 = utils.shasum(path)
filename = os.path.basename(path)
filesize = os.path.getsize(path)

print 'uploading %s (branch %s / revision %s)...' % (filename, branch, revision)
key = Key(bucket)
key.key = '%s/%s/%s' % (type, branch, filename)
key.set_metadata('git_revision', revision)
key.set_metadata('git_branch', branch)
key.set_metadata('build_url', build_url)
key.set_metadata('build_type', type)
key.set_metadata('sha1', sha1)

max_retries = 5
uploaded = False
for i in range(1, max_retries+1):
	try:
		key.set_contents_from_filename(path)
		print "-> succesfully uploaded on attempt #%d" % i
		uploaded = True
		break
	except socket.error, e:
		if i <= max_retries:
			print '-> received error: %s, retrying upload (attempt #%d)...' % (str(e), i+1)

if not uploaded:
	print >>sys.stderr, "Failed to upload %s after %d attempts" % (path, max_retries)
	sys.exit(1)

key.make_public()

print 'updating %s/%s/index.json..' % (type, branch)
index_key = bucket.get_key('%s/%s/index.json' % (type, branch))
index = []
if index_key == None:
	index_key = Key(bucket)
	index_key.key = '%s/%s/index.json' % (type, branch)
else:
	index = simplejson.loads(index_key.get_contents_as_string())

index.append({ 'filename': filename, 'git_branch': branch, 'git_revision': revision, 'build_url': build_url, 'build_type': type, 'sha1': sha1, 'size': filesize })
index_key.set_contents_from_string(simplejson.dumps(index))
index_key.make_public()
