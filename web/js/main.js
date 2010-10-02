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
					.append(date.format('mmm d yyyy HH:MM') + " ")
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
				.append($('<div/>').addClass('sha1').text('filename: '+file.filename))
				.append($('<div/>').addClass('sha1').text('sha1: '+file.sha1)))
			.append($('<td/>').text(size));
		$('#'+type+'_table').append(row);
	}
	
	function loadBranches(type, branches) {
		var select = $('#'+type+'_branch');
		select.empty();
		select.attr('disabled', null);
		$.each(branches, function(index, branch) {
			var option = $('<option></option>').attr('value', branch).text(branch);
			if (branch == "master") {
				$(option).attr("selected", "selected");
			}
			select.append(option);
		});
		select.change(function() {
			var branch = select.val();
			var table = $('#'+type+'_table');
			table.empty();
			$.getJSON(type+'/'+branch+'/index.json', function(data) {
				loadTable(type, data);
			});
		});
	}
	
	function loadTable(type, data) {
		var revisions = {};
		var revisionIndexes = [];
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

		var i = 0;
		$.each(revisions, function(revision, files) {
			revisionIndexes[i++] = revision;
		});

		revisionIndexes.sort(function(a, b) {
			return revisions[a][0].date - revisions[b][0].date;
		});
		revisionIndexes.reverse();
		
		$.each(revisionIndexes, function(index, revision) {
			appendRevision(type, revision, revisions[revision]);
		});
	}
	
	$('body').ajaxError(function(event, xhr, settings, exception) {
		var type = settings.url.substring(0, settings.url.lastIndexOf('/'));
		$('#'+type+'_table').html('<tr><td>No builds found</td></tr>');
	});

	// master is the default branch	
	$.getJSON("mobile/branches.json", function(data) {
		loadBranches('mobile', data);
	});
	$.getJSON('mobile/master/index.json', function(data) {
		loadTable('mobile', data);
	});
	$.getJSON("desktop/branches.json", function(data) {
		loadBranches('desktop', data);
	});
	$.getJSON('desktop/master/index.json', function(data) {
		loadTable('desktop', data);
	})
});
