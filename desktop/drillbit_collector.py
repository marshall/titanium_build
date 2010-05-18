#!/usr/bin/python
import os, sys, platform, simplejson

platforms = { "Windows": "win32", "Darwin": "osx", "Linux": "linux" }
build_platform = platforms[platform.system()]

drillbit_dir = os.path.join('build', build_platform, 'Drillbit')
contents_dir = drillbit_dir
if build_platform == 'osx':
	drillbit_dir += ".app"
	contents_dir = os.path.join(drillbit_dir, "Contents")

test_results_dir = os.path.join(contents_dir, "Resources", "test_results")


total_success = 0
total_failed = 0
total = 0
failures = []

def get_results(suite, json):
		global total_success, total_failed, total, failures
		total_success += json["success"]
		total_failed += json["failed"]
		total += json["count"]
		if json["failed"] > 0:
			for result in json["results"]:
				if not result["passed"]:
					failures.append(result)

for file in os.listdir(test_results_dir):
	if file.endswith(".json") and file != "drillbit.json":
		suite = file[0:-5]
		json = simplejson.loads(open(os.path.join(test_results_dir, file), 'r').read())
		get_results(suite, json)

data = {"total_success":total_success,"total_failed":total_failed,"total":total,"failures":failures}

failures_html = "<hr/>"
for failure in failures:
	failures_html += "<span class=\"failure\"><b>%s</b><br/>line %s: %s</span><hr/>\n" % (failure["name"], failure["lineNumber"], failure["message"])

html = """
<html>
<head>
	<style>
		* { font-size: 16px; font-family: sans-serif }
		.passed { color: #393; font-weight: bold; }
		.failed { color: #933; font-weight: bold; }
		.failure { color: #933; }
	</style>
</head>
<body>
	<b>Total passed tests</b>: <span class="passed">%s</span><br/>
	<b>Total failed tests</b>: <span class="failed">%s</span><br/>
	%s
</body>
</html>
""" % (total_success, total_failed, failures_html)

print html
