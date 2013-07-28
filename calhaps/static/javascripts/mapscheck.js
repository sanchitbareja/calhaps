var map;
var mapOptions; 
var mapCenter;
var marker;

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



   marker = new google.maps.Marker({
      position: myLatlng,
      map: map,
      animation: google.maps.Animation.DROP,
      draggable: false,
      visible:true
  });

   var boxText = document.createElement("div");
   boxText.style.cssText = "border: 5px solid gray; margin-top: 8px; background: white; padding: 5px;"; 
    boxText.innerHTML = "City Hall, Sechelt<br>British Columbia<br>Canada"; 
               
    var myOptions = {
                 content: boxText
                ,disableAutoPan: false
                ,maxWidth: 0
                ,pixelOffset: new google.maps.Size(-140, 0)
                ,zIndex: null
                ,boxStyle: { 
                  background: "url('/site_media/static/images/tipbox.gif') no-repeat"
                  ,opacity: 1
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
        ib.open(map, marker);
        google.maps.event.addListener(marker, 'click',toggleBounce);

}

function toggleBounce(){
   if (marker.getAnimation() != null) {
    marker.setAnimation(null);
  } else {
    marker.setAnimation(google.maps.Animation.BOUNCE);
  }
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





                
        