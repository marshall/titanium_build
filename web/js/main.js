$(document).ready(function() {
	var descriptions = {
		mobile: {
			osx: "OSX (iPhone, Android)",
			linux: "Linux (Android only)",
			win32: "Windows (Android only)"
		},
		desktop: {osx: "OSX", linux: "Linux", win32: "Windows"}
	};
	var mobileGitUrl = "http://github.com/appcelerator/titanium_mobile/commit/";
	var desktopGitUrl = "http://github.com/appcelerator/titanium_desktop/commit/";
	
	function appendRevision(type, revision, files) {
		var url = (type=="mobile" ? mobileGitUrl : desktopGitUrl) + revision;
		
		var date = new Date();
		if (files.length > 0) {
			date = files[0].date;
		}
		
		var shortRevision = revision.substring(0,8);
		var row = $('<tr/>').addClass('revision')
			.append($('<th/>')
					.append(date)
					.append($('<a/>').attr('href', url).text('r'+shortRevision)))
			.append($('<th/>').text('Size'))
		$('#'+type+'_table').append(row);
		
		$.each(files, function(index, file) {
			appendFile(type, revision, file);
		});
	}
	
	function getPlatform(file) {
		var last = file.filename.split("-")[3];
		return last.substring(0, last.length-4);
	}
	
	function appendFile(type, revision, file) {
		var platform = getPlatform(file);
		var platformDesc = descriptions[type][platform];
		var size = "" + Math.round(file.size/1024.0/1024.0*100.0)/100.0 + " MB";
		var fileUrl = 'http://builds.appcelerator.com.s3.amazonaws.com/' + type + '/' + file.filename;
		var row = $('<tr/>')
			.append($('<td/>')
				.append($('<img/>').attr('src', 'images/'+platform+'.png'))
				.append($('<a/>').attr('href', fileUrl).text(platformDesc))
				.append($('<div/>').addClass('sha1').text('sha1: '+file.sha1)))
			.append($('<td/>').text(size));
		$('#'+type+'_table').append(row);
	}
	
	function loadTable(type, data) {
		var revisions = {};
		for (var i = 0; i < data.length; i++) {
			var file = data[i];
			var timestamp = file.filename.split("-")[2];
			var date = new Date();
			date.setFullYear(timestamp.substring(0,4), timestamp.substring(4,6)-1, timestamp.substring(6,8));
			date.setHours(timestamp.substring(8,10));
			date.setMinutes(timestamp.substring(10,12));
			date.setSeconds(timestamp.substring(12,14));
			file.date = date;
			
			var revision = file.git_revision;
			if (!(revision in revisions)) {
				revisions[revision] = [];
			}
			revisions[revision].push(file);
		}
		
		$.each(revisions, function(revision, files) {
			appendRevision(type, revision, files);
		});
	}
	
	$.getJSON('mobile/index.json', function(data) {
		loadTable('mobile', data);
	});
	$.getJSON('desktop/index.json', function(data) {
		loadTable('desktop', data);
	})
});