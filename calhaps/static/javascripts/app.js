//////////////////////////////////////////
//////////// Global Variables ////////////
//////////////////////////////////////////

var display_date = new Date(); // will need to increment/decrement dates depending on what they request. start with current_date
var all_filters = ['Parties','Concerts','Greeklife','Sports','Philanthropy','Performances','Conferences','Movies','Food','Green','Celebrity','Exhibitions','Others']
var list_id = '#filteredList'
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
			update_list_and_map(data['response']['events']);
			console.log(display_date);
			update_date_display();
		}
	});
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
		current_date = ""+current_date+"st";
	}
	else if(current_date == 2){
		current_date = ""+current_date+"nd";
	}
	else if(current_date == 3){
		current_date = ""+current_date+"rd";
	}
	else {
		current_date = ""+current_date+"th";
	}
	$("#filteredDateDisplay").text(current_date+" "+current_day);
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

	if(filters){
		filters = all_filters;
	}

	return filters
}

function toggle_switch(label_for, element) {
	if($(element).is(":checked")){
		$("label[for="+label_for+"]").parent().css('background','white');
		$("label[for="+label_for+"]").css('color','black');
	} else {
		$("label[for="+label_for+"]").parent().css('background','transparent');
		$("label[for="+label_for+"]").css('color','white');
	}

	// refresh list based on filter
	event_filters = get_filters();
	response_events = get_events_and_update_ui(textify_filters(event_filters), textify_date());
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

function attach_events_to_markers(marker, newli, event_object){
	var contentInfo = 	'<div id="markerContentInfo"><div id="tipBox"></div>'+
							'<div id="markerContentHeader">'+
								'<div id="markerContentHeaderText">'+event_object['title']+
									', <a href="javascript:;"'+event_object['club']['id']+'</a>'+
								'</div>'+
							'</div>'+
							'<br/><div id="markerContentWhereWhenDiv">'+
							'<p class="radius success label" id="markerContentWhereWhenText">@ '+event_object['location']['name']+', '+formatAMPM(new Date(event_object['startTime']))+'</p>'+
							'<br /></div>'+
							'<div id="markerContentMainText">'+
								'<img id="markerContentImage" src="'+event_object['imageUrl']+'" />'+
								'<p>'+event_object['description']+'</p>'+
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
			height:"130px",
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

function create_list_element(event_object) {
	var list_item = $.parseHTML('<li><a href="javascript:;"><i class="foundicon-smiley" style="margin-bottom:0px; margin-right:10px;"></i> '+event_object['title']+'</a></li>');
	$(list_id).append(list_item);
	return list_item[0];
}


function create_marker(event_object) {
	var newMarkerPos = new google.maps.LatLng(event_object['location']['lat'],event_object['location']['lng']);
	var marker = new google.maps.Marker({
	    map:map,
	    draggable:false,
	    animation: google.maps.Animation.DROP,
	    position: newMarkerPos,
	    title:event_object['title']
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
     	console.log("hello");
  	};
  	document.body.appendChild(script);
}

$(document.body).ready(loadScript);
