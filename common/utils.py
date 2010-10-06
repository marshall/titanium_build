import os, sys, re
import simplejson
from subprocess import Popen, PIPE
from boto.s3.connection import S3Connection
from boto.s3.key import Key

class Config(object):
	def __init__(self, file=None):
		if file != None:
			self.json = simplejson.loads(open(file, 'r').read())
		else:
			self.json = {}

	def get_aws_key(self):
		return self.get('AWS_KEY')
	
	def get_aws_secret(self):
		return self.get('AWS_SECRET')

	def get_upload_bucket(self):
		return self.get('UPLOAD_BUCKET')

	def open_bucket(self):
		conn = S3Connection(self.get_aws_key(), self.get_aws_secret())
		return conn.get_bucket(self.get_upload_bucket())

	def verify_aws(self):
		return self.get_aws_key() != None and self.get_aws_secret() != None
		
	def get(self, property):
		if property in self.json:
			return self.json[property]
		elif property in os.environ:
			return os.environ[property]
		else: return None

def get_build_config():
	config_json = os.path.join(os.path.dirname(
		os.path.abspath(os.path.dirname(__file__))), 'config.json')
	return Config(config_json)

def shasum(path):
	out = Popen(['shasum', path], stdout=PIPE).communicate()[0]
	return re.split(r' *', out.rstrip())[0]

def get_key_json_object(bucket, key, default=None):
	key_obj = bucket.get_key(key)
	if key_obj == None:
		key_obj = Key(bucket)
		key_obj.key = key
	else:
		return simplejson.loads(key_obj.get_contents_as_string())
	if default == None: return {}
	else: return default

def set_key_json_object(bucket, key, object):
	key_obj = bucket.get_key(key)
	if key_obj == None:
		key_obj = Key(bucket)
		key_obj.key = key

	key_obj.set_contents_from_string(simplejson.dumps(object))
	key_obj.make_public()
