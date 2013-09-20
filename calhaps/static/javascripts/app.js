//////////////////////////////////////////
//////////// Global Variables ////////////
//////////////////////////////////////////

var display_date = new Date(); // will need to increment/decrement dates depending on what they request. start with current_date
var all_filters = ['Parties','Concerts','Greeklife','Sports','Philanthropy','Performances','Conferences','Movies','Food','Green','Celebrity','Exhibitions','Others']
var list_id = '#filteredList';
var favorite_list_id = '#favorited_events';
var pins_id = '#pin-columns';
var number_of_events_id = '#number_events';
var map;
var mapCenter;
var mapOptions;
var markers = [];

//////////////////////////////////////////
//////////// Helper Functions ////////////
//////////////////////////////////////////

function textify_filters (filters_array) {
	return filters_array.join(',');
}

function textify_date(){
	// converts the current date into text that the API will accept
	return ""+display_date.getFullYear()+"-"+(display_date.getMonth()+1)+"-"+display_date.getDate();
}

function to_today_date(){
	display_date = new Date();
}

function next_date(){
	// changes to the next day
	display_date.setDate(display_date.getDate() + 1);
}

function previous_date(){
	// changes to the previous day
	display_date.setDate(display_date.getDate() - 1);
}

function next_week_date(){
	// changes to the next week
	display_date.setDate(display_date.getDate() + 7);
}

function formatAMPM(date) {
	var hours = date.getHours();
	var minutes = date.getMinutes();
	var ampm = hours >= 12 ? 'pm' : 'am';
	var hours = hours % 12;
	hours = hours ? hours : 12; // the hour '0' should be '12'
	minutes = minutes < 10 ? '0'+minutes : minutes;
	day = date.getDate();
	month = date.getMonth() + 1;
	strTime = month+"/"+day+", "+hours + ':' + minutes + ' ' + ampm;
	return strTime;
}

//////////////////////////////////////////
////////// Update UI Functions ///////////
//////////////////////////////////////////

function get_events_and_update_ui(filters_text, date) {
	// returns events from query
	console.log(filters_text);
	console.log(date);
	$.ajax({
		type: "GET",
		url: '/api/v1/events/',
		data: {
			'event_filters': filters_text,
			"date": date
		},
		success: function(data, status, xhr) {
			console.log(data);
			console.log(status);
			update_number_of_events(data['response']['events']);
			update_list_and_map(data['response']['events']);
			update_grid(data['response']['events']);
			update_favorite_events(data['response']['events']);
			console.log(display_date);
			update_date_display();
		}
	});
}

function post_favorite_and_update_ui(event_id){
	user_id = $("#user_id").val();
	$.ajax({ 
      url:'/api/v1/favorites/', 
      type:'POST',
      dataType: 'json',
      data: JSON.stringify({
        'event': event_id, 
        'user': user_id
      }), 
      contentType: 'application/json',
      statusCode : {
        201: function(data, textStatus, jsXHR){
          console.log("Successfully favorited company!");
          //update UI for that particular event_id here.
        }
      }
    });
}

function update_event_modal(title, description, image_url, location_name, start_time, club_name, club_description, club_image_url){
	console.log(title);
	console.log(description);
	console.log(image_url)
	console.log(location_name);
	console.log(start_time);
	console.log(club_name);
	console.log(club_description);
	console.log(club_image_url);
	$("#eventModalTitle").text(title);
	$("#eventModalDescription").text(description);
	if(image_url){
		$("#eventInfoModal").css("background","url(\'"+image_url+"\')");
	}
	$("#eventModalLocationName").text(location_name);
	$("#eventModalStartTime").text(formatAMPM(new Date(start_time)));
	$("#eventModalClubName").text(club_name);
	$("#eventModalClubDescription").text(club_description);
	if(club_image_url){
		$("#eventModalClubImage").attr("src",club_image_url);
	}
}

function update_date_display() {
	var weekday=new Array(7);
	weekday[0]="Sunday";
	weekday[1]="Monday";
	weekday[2]="Tuesday";
	weekday[3]="Wednesday";
	weekday[4]="Thursday";
	weekday[5]="Friday";
	weekday[6]="Saturday";

	var current_day = weekday[display_date.getDay()];
	var current_date = display_date.getDate();
	if(current_date == 1){
		current_date = ""+current_date+"st "+current_day;
	}
	else if(current_date == 2){
		current_date = ""+current_date+"nd "+current_day;
	}
	else if(current_date == 3){
		current_date = ""+current_date+"rd "+current_day;
	}
	else {
		current_date = ""+current_date+"th "+current_day;
	}

	if(display_date.getFullYear() == (new Date()).getFullYear() && display_date.getMonth() == (new Date()).getMonth() && display_date.getDate() == (new Date()).getDate()){
		current_date = "Today";
	} 

	$("#filteredDateDisplay").text(current_date);
	$("#noOfEventsDateDisplay").text(current_date.toLowerCase());
}

//////////////////////////////////////////
///////// UI Triggered Functions /////////
//////////////////////////////////////////

function get_filters() {
	var filters = [];
	if($("input[id=toggle-all]").is(":checked")) {
		filters = all_filters;
	} else {
		$("input[id^=toggle]").each(function(index,element) {
			if($(element).is(":checked")) {
				console.log(element);
				filters.push($(element).val());
			}
		});
	}

	if(filters.length == 0){
		filters = all_filters;
	}

	return filters
}

function toggle_switch(label_for, element) {
	if($(element).is(":checked")){
		$("label[for="+label_for+"]").parent().css('background','rgba(40,40,40,0.8)');
		$("label[for="+label_for+"]").css('color','white');
	} else {
		$("label[for="+label_for+"]").parent().css('background','transparent');
		$("label[for="+label_for+"]").css('color','#aaa');
	}

	// refresh list based on filter
	event_filters = get_filters();
	response_events = get_events_and_update_ui(textify_filters(event_filters), textify_date());
}

function update_number_of_events(events){
	// updates the number of events counter
	$(number_of_events_id).text(events.length);
}

function update_list_and_map(events) {
	//this method removes all the current events in the list and updates it with the new set of elements

	//empty the current list and delete all existing markers
	$(list_id).empty();
	delete_markers();

	// add stuff to list and add markers to map
	for (var i in events) {
		
		new_list_item = create_list_element(events[i]);
		new_marker = create_marker(events[i]);
		attach_events_to_markers(new_marker, new_list_item, events[i]);

		console.log('updating map');
	};
}

function update_grid(events) {
	//this method removes all the current events in the grid and updates it with the new set of elements

	//empty the current list and delete all existing markers
	$(pins_id).empty();

	// add stuff to list and add markers to map
	for (var i in events) {
		if(events[i]['imageUrl']){
			new_grid_item = create_grid_element(events[i]);
		}
		console.log('updating grid');
	};
}

function update_favorite_events(events){
	user_id = parseInt($("#user_id").val());
	console.log("update_favorite_events");
	console.log(user_id);
	for (var i in events) {
		console.log(events[i]["favorites"]);
		if(events[i]["favorites"].indexOf(user_id) > -1){
			$(favorite_list_id).append($.parseHTML('<li><a href="#" data-reveal-id="eventInfoModal" onclick="update_event_modal(\''+events[i]['title']+'\',\''+events[i]['description']+'\',\''+events[i]['imageUrl']+'\',\''+events[i]['location']['name']+'\',\''+events[i]['startTime']+'\',\''+events[i]['club']['name']+'\',\''+events[i]['club']['description']+'\',\''+events[i]['club']['imageUrl']+'\')">'+events[i]['title'].substr(0,15)+'</a></li>'));
		}
		console.log('updating favorites');
	};
}

function attach_events_to_markers(marker, newli, event_object){
	var contentInfo = 	'<div id="markerContentInfo"><div id="tipBox"></div>'+
							'<div id="markerContentHeader">'+
								'<div id="markerContentHeaderText">'+event_object['title'].substr(0,20)+
									', '+event_object['club']['name']+''+
								'</div>'+
							'</div>'+
							'<div id="markerContentMainText">'+
								'<img id="markerContentImage" src="'+event_object['imageUrl']+'" />'+
								'<p>'+event_object['description'].substr(0,150)+'...'+
								'<a href="#" data-reveal-id="eventInfoModal" onclick="update_event_modal(\''+event_object['title']+'\',\''+event_object['description']+'\',\''+event_object['imageUrl']+'\',\''+event_object['location']['name']+'\',\''+event_object['startTime']+'\',\''+event_object['club']['name']+'\',\''+event_object['club']['description']+'\',\''+event_object['club']['imageUrl']+'\')"> More</a>'+
							'</div>'+
							'<div id="markerContentWhereWhenDiv">'+
								'<p class="success label" id="markerContentWhereWhenText">@ '+event_object['location']['name'].substr(0,12)+', '+formatAMPM(new Date(event_object['startTime']))+'</p>'+
							'</div>'+
						'</div>';

	//handling what happens when marker is clicked
	function toggleClick() {
		if(ib.getMap()){
			ib.close();				
		} else {
			ib.open(map,marker);
		}
	}

	function toggleBounce() {
		if(marker.getAnimation() == null){
			marker.setAnimation(google.maps.Animation.BOUNCE);
		} else {
			marker.setAnimation(null);
		}
	}

	var myOptions = {
		 content: contentInfo
		,pixelOffset: new google.maps.Size(-160, 0)
		,boxStyle: {
			background: "white",
			width:"300px",
			height:"140px",
			opacity: 1.0
		}
		,disableAutoPan: false
		,maxWidth: 300
		,closeBoxURL: "http://www.google.com/intl/en_us/mapfiles/close.gif"
		,infoBoxClearance: new google.maps.Size(100, 100)
		,isHidden: false
		,pane: "floatPane"
		,enableEventPropagation: true
	};

	var ib = new InfoBox(myOptions);

	//add listener to the marker
	google.maps.event.addListener(marker, "click", toggleClick);
	//attaching events to list items in sidebar
	google.maps.event.addDomListener(newli,'click', toggleClick);
	google.maps.event.addDomListener(newli,'mouseover', toggleBounce);
	google.maps.event.addDomListener(newli,'mouseout', toggleBounce);
}

function disable_button(element){
	$(element).addClass("disabled");
	$(element).text("Favorited");
}

function create_list_element(event_object) {
	user_id = parseInt($("#user_id").val());
	var list_item = $.parseHTML('<li><a class="button tiny secondary" href="#" onclick="post_favorite_and_update_ui(\''+event_object['id']+'\'); disable_button(this);" >Favorite </a><a href="javascript:;"><i class="foundicon-smiley" style="margin-bottom:0px; margin-right:10px;"></i> '+event_object['title'].substr(0,15)+'</a></li>');
	if(event_object["favorites"].indexOf(user_id) > -1){
		list_item = $.parseHTML('<li><a class="button tiny secondary disabled" href="#">Favorited </a><a href="javascript:;"><i class="foundicon-smiley" style="margin-bottom:0px; margin-right:10px;"></i> '+event_object['title'].substr(0,15)+'</a></li>');
	}	
	$(list_id).append(list_item);
	return list_item[0];
}

function create_grid_element(event_object) {
	user_id = parseInt($("#user_id").val());
	var favorite_item = '<a href="#" class="button tiny secondary" onclick="post_favorite_and_update_ui(\''+event_object['id']+'\'); disable_button(this);" >Favorite! </a>';
	if(event_object["favorites"].indexOf(user_id) > -1){
		favorite_item = '<a class="button tiny secondary disabled" href="#">Favorited </a>';
	}
	var grid_item = $.parseHTML('<a href="#" data-reveal-id="eventInfoModal" onclick="update_event_modal(\''+event_object['title']+'\',\''+event_object['description']+'\',\''+event_object['imageUrl']+'\',\''+event_object['location']['name']+'\',\''+event_object['startTime']+'\',\''+event_object['club']['name']+'\',\''+event_object['club']['description']+'\',\''+event_object['club']['imageUrl']+'\')">'+
		'<div class="pin">'+
          '<img style="min-height:8em;width:inherit;" src="'+event_object['imageUrl']+'" />'+
          '<div class="pin-text">'+
            '<h5 class="grid_title">'+event_object['title'].substr(0,20)+'</h5>'+
            '<p class="grid_text">@'+event_object['location']['name'].substr(0,12)+
            favorite_item+'</p>'+
          '</div>'+
        '</div></a>');
	$(pins_id).append(grid_item);
	return grid_item[0];
}

function create_marker(event_object) {
	var newMarkerPos = new google.maps.LatLng(event_object['location']['lat'],event_object['location']['lng']);
	var marker = new google.maps.Marker({
	    map:map,
	    draggable:false,
	    animation: google.maps.Animation.DROP,
	    position: newMarkerPos,
	    title:event_object['title'].substr(0,20)
	});

	console.log(newMarkerPos);
	markers.push(marker);
	return marker;
}

function delete_markers() {
	//remove existing markers and lists
	for (var i = markers.length - 1; i >= 0; i--) {
		markers[i].setMap(null);
	};
}

//////////////////////////////////////////
///////////// Initialization /////////////
//////////////////////////////////////////

function initialize(){
     var scriptInfoBox = document.createElement("script");
     scriptInfoBox.type = "text/javascript";
     scriptInfoBox.src = "http://google-maps-utility-library-v3.googlecode.com/svn/trunk/infobox/src/infobox.js";
     document.body.appendChild(scriptInfoBox); /* Need to make it cross-browser safe */
     scriptInfoBox.onload=initializeMap;
     // add all events from today
	response_events = get_events_and_update_ui(textify_filters(all_filters), textify_date());
 }

function initializeMap() {
 
  	var myLatlng = new google.maps.LatLng(37.87201, -122.25775);
  	mapCenter= myLatlng;
   	mapOptions = {
	    zoom: 15,
	    center: mapCenter,
	    mapTypeId: google.maps.MapTypeId.ROADMAP
	};
  	map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

   	// add all events from today
	response_events = get_events_and_update_ui(textify_filters(all_filters), textify_date());
}

function loadScript() {
  	console.log("hello0");
  	var script = document.createElement('script');
  	script.type = 'text/javascript';
  	script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyAdKiY3Szf1k-5KA4oTbslJrg3RPrna2rQ&sensor=false&callback=initialize';
  	script.onload = function() {
     	initialize();
  	};
  	document.body.appendChild(script);
}

$(document.body).ready(loadScript);
