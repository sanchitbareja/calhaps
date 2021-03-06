# API Reference for Calhaps

This is the `/v1/` API documentation for the Calhaps API. All requests are RESTful and all request and response bodies are `json` formatted.

*	[Login User](#loginuser)
* 	[Get Clubs](#getclubs)
* 	[Get Events](#getevents)
* 	[Post Event](#postevent)

##<a id="loginuser"></a>Login User

Authenticates the user using Facebook. Retrieves permissions as well.

##<a id="getclubs"></a>Get Clubs

Returns a list of clubs

HTTP Method: GET
Requires Authentication: No

URL: `/api/v1/clubs/`

Content-type: `application/json`
Filtering options:

Example response:

	{
		"meta": {
        	"limit": 1000,
        	"next": null,
        	"offset": 0,
        	"previous": null,
        	"total_count": 2
    	},
    	"response": {
    		"clubs": [{
    			"id": "2",
    			"name": "Alpha Beta Gamma",
    			"description": "This club wishes to foster brotherhood.",				"typeOfOrganization": "Social Fraternity",
    			"founded": "mm/dd/yyyy",
    			"urlPersonal": "http://www.alphabetagamme.com",
    			"imageUrl": "http://calhaps.amazonaws.com/alphabetagamma_logo.jpg"
    		}, {
    			"id": "2",
				"name": "Theta Beta Gamma",
    			"description": "This is where Nerd rules!",    				"typeOfOrganization": "Academic Fraternity",
    			"founded": "mm/dd/yyyy",
    			"urlPersonal": "http://www.nerdrulez.com"",
    			"imageUrl": "http://calhaps.amazonaws.com/nerds_are_awesome.png"
    		}]
    	}
	}
	
##<a id="getevents"></a>Get Events

Returns a list of events

HTTP Method: GET
Requires Authentication: No

URL: `/api/v1/events/`

Content-type: `application/json`
Filtering options: `date`, `event_filters`

	e.g. /api/v1/events/?date=2013-08-01&event_filters=parties,conferences

Example response:

	{
		"meta": {
        	"limit": 1000,
        	"next": null,
        	"offset": 0,
        	"previous": null,
        	"total_count": 2
    	},
    	"response": {
    		"events": [{
    			"title": "Boogie Night!",
    			"description": "Enjoy a night of games!",
    			"startTime": "mm/dd/yyyy - HH:MM"
    			"club": {
    				"id": "2",
					"name": "Theta Beta Gamma",
    				"description": "This is where Nerd rules!",    					"typeOfOrganization": "Academic Fraternity",
    				"founded": "mm/dd/yyyy",
    				"urlPersonal": "http://www.nerdrulez.com"",
    				"imageUrl": "http://calhaps.amazonaws.com/nerds_are_awesome.png"
    			},
    			"location": {
    					"name": "TDX",
    					"lat": "152.111",
    					"lng": "142.23"
    			},
    			"imageUrl": "http://calhaps.amazonaws.com/boogienight.jpg",
    			"typeOfEvent": [{
    				"type": "Party"
    			}, {
    				"type": "Sports"
    			}],
    			"advertise": "mm/dd/yyyy"
    		}, {
    			"title": "Drinks Night!",
    			"description": "Enjoy a night of drinks!",
    			"startTime": "mm/dd/yyyy - HH:MM"
    			"club": {
    				"id": "2",
					"name": "Theta Beta Gamma",
    				"description": "This is where Nerd rules!",    					"typeOfOrganization": "Academic Fraternity",
    				"founded": "mm/dd/yyyy",
    				"urlPersonal": "http://www.nerdrulez.com"",
    				"imageUrl": "http://calhaps.amazonaws.com/nerds_are_awesome.png"
    			,
    			"location": {
		    			"name": "TDX",
    					"lat": "152.111",
    					"lng": "142.23"
    			},
    			"imageUrl": "http://calhaps.amazonaws.com/drinksfreeflow.png",
    			"typeOfEvent": [{
    				"type": "Sports"
    			}],
    			"advertise": "None"
    		}]
    	}
	}
	
##<a id="postevent"></a>Post Event

Post a new event

Example Request Body:

	{
		"title": "A super cool title!",
		"description": "And equally cool description!"
		"addedBy": "sanchitbareja@gmail.com" (optional, if they want to get a notification)
	}

Example RESPONSE header:

	Status Code: 201
	Date: Fri, 19 Jul 2013 22:52:43 GMT
	Server: WSGIServer/0.1 Python/2.7.2
	Vary: Accept
	Content-Type: application/json

Example RESPONSE body:

	{

	}