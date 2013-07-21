 var map;
var mapOptions; 
var mapCenter;
var markers[];

function initialize(){
     var scriptInfoBox = document.createElement("script");
     scriptInfoBox.type = "text/javascript";
     scriptInfoBox.src = "http://google-maps-utility-library-v3.googlecode.com/svn/trunk/infobox/src/infobox.js";
     document.body.appendChild(scriptInfoBox); /* Need to make it cross-browser safe */
     scriptInfoBox.onload=initializeMap;
 }

function initializeMap() {
 
  var myLatlng= new google.maps.LatLng(37.87201, -122.25775);
  mapCenter= myLatlng;
   mapOptions = {
    zoom: 15,
    center: mapCenter,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);


  $.ajax({
        type: "POST",
        url: "/api/v1/event/?format=json"
    }).done(function(data){

        for(var new_event in data["objects"){
          var newMarkerPos = new google.maps.LatLng(data["objects"][new_event]["location"]["lat"],data["objects"][new_event]["location"]["lng"]);
          var marker = new google.maps.Marker({
              map:map,
              draggable:false,
              animation: google.maps.Animation.DROP,
              position: newMarkerPos,
              title:data["objects"][new_event]["title"]
          });

          markers.push(marker);

          var oldul = document.querySelectorAll("#nlists")[0];
          var newa = document.createElement("a");
          newa.className = "eventInformation";
          var eventTitle = document.createElement("p");
          eventTitle.className = "eventTitle";
          eventTitle.appendChild(document.createTextNode(marker.getTitle()));
          newa.appendChild(eventTitle);
          newa.appendChild(document.createTextNode("By "+data["objects"][new_event]["club"]["name"]+", @"+data["objects"][new_event]["location"]["name"]+", "+formatAMPM(new Date(data["objects"][new_event]["startTime"]))));
          var newli = document.createElement("li");
          if(data["objects"][new_event]["advertise"]){
            newli.id = "eventAdvertise";
          } else{
            newli.id = "eventNormal";
          }

          // newli.className = "head";
          newli.appendChild(newa);
          oldul.appendChild(newli);

          attachEventsToMarkers(marker,
            data["objects"][new_event]["id"],
            data["objects"][new_event]["title"],
            data["objects"][new_event]["description"],
            data["objects"][new_event]["image"],
            /*data["objects"][new_event]["numberOfRagers'],*/
            data["objects"][new_event]["location"]["name"],
            data["objects"][new_event]["startTime"],
            data["objects"][new_event]["club"]["id"],
            data["objects"][new_event]["club"]["name"], /*["host"]*/
            newli);
        }   
    });
}


function attachEventsToMarkers(marker,eventID,eventName,eventDescription,image,numberOfRagers,where,startTime,hostid,host,newli)
{
  var contentBox =   '<div id="markerContentInfo"><div id="tipBox"></div>'+
              '<div id="markerContentHeader">'+
                '<div id="markerContentHeaderText">'+eventName+
                  ', <a href="javascript:;" onclick=getClubInfo('+hostid+')>'+host+'</a>'+
                '</div>'+
              '</div>'+
              '<br/><div id="markerContentWhereWhenDiv">'+
              '<p class="radius success label" id="markerContentWhereWhenText">@ '+where+', '+formatAMPM(new Date(startTime))+'</p>'+
              '<br /></div>'+
              '<div id="markerContentMainText">'+
                '<img id="markerContentImage" src="'+image+'" />'+
                '<p>'+eventDescription+'</p><p id="eventLink">&hellip;<a href="/event/'+eventID+'" target="_blank"/>More on the event</a>'+
              '</div>'+
              '<div class="rageContainer">'+
                '<div id="rageID_'+eventID+'">'+
                  '<a href="javascript:;" class="rageButton" onclick=sendRageRequest('+eventID+')>&#9996; </a>'+
                  numberOfRagers+' others raged here'+
                '</div>'+
              '</div>'+
            '</div>';
}
  
    var myOptions = {
                 content: contentBox
                ,disableAutoPan: false
                ,maxWidth: 0
                ,pixelOffset: new google.maps.Size(-140, 0)
                ,zIndex: null
                ,boxStyle: { 
                  background: "url('tipbox.gif') no-repeat"
                  ,opacity: 0.75
                  ,width: "280px"
                 }
                ,closeBoxMargin: "10px 2px 2px 2px"
                ,closeBoxURL: "http://www.google.com/intl/en_us/mapfiles/close.gif"
                ,infoBoxClearance: new google.maps.Size(1, 1)
                ,isHidden: false
                ,pane: "floatPane"
                ,enableEventPropagation: false
        };

        var ib = new InfoBox(myOptions);

        /*
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
        }*/

        /*google.maps.event.addListener(marker, "click", toggleClick);
          //attaching events to list items in sidebar
        google.maps.event.addDomListener(newli,'click', toggleClick);
        google.maps.event.addDomListener(newli,'mouseover', toggleBounce);
        google.maps.event.addDomListener(newli,'mouseout', toggleBounce);*/
        
}



function loadScript() {
  
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyAdKiY3Szf1k-5KA4oTbslJrg3RPrna2rQ&sensor=true&callback=initialize';
  document.body.appendChild(script);
    script.onload = function() {
       
    };
}
window.onload=loadScript;





                
        