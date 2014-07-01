/*
Title: Audio content object (jQuery)
Version: 0.1
*/

(function() {
	"use strict";

	//Initialize SoundCloud client
	SC.initialize({
		client_id: '58fe853bbce5a66043c13f27fff9ce68'
	});

	$(".audio").each(function () {
		//Player state flag
		var isPaused = true;
		
		//jQuery selectors
		var $this = $(this);
		var $playButton = $this.find(".audio-play");
		var $stopButton = $this.find(".audio-stop");
		
		//Get track ID
		var trackID = $this.attr("data-soundcloudID");
		
		//Set up basic SoundCloud player using SDK
		SC.stream("/tracks/" + trackID, function(sound){
			//var test;
			$playButton.click(function () {
				if (isPaused) {
					sound.play();
					$playButton.html("Pause");
					isPaused = false;
				} else {
					sound.pause();
					$playButton.html("Play");
					isPaused = true;
				}
			});
			$stopButton.click(function () {
				sound.stop();
				$playButton.html("Play");
				isPaused = true;
			});
		});
		
		//Get track data
		SC.get("/tracks/" + trackID, function (data) {
			//Set data in player
			//document.getElementById("scTitle").innerHTML = data.title; 
			$this.find("h2").find("a").attr("href", data.permalink_url);
			$this.find(".audio-author-link").attr("href", data.user.permalink_url).html(data.user.username);
		});
	});
})();
