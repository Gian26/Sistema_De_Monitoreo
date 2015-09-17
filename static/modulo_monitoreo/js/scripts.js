$(function(){
	if(navigator.geolocation){
		navigator.geolocation.getCurrentPosition
	}else{
		initialize(33.30,-87.0933);
	}
	
	function getCoords(position)
	{
		var lat = position.coords.latitude;
		var lng = position.coords.longitude;

		initialize(lat,lng);
	
	}

	function initialize(lat, lng){
		var latlng = new google.maps.LatLng(lat,lng);
		var mapSettings = {
			center: latlng,
			zoom:18,
			mapTypeId:google.maps.mapTypeId.ROADMAP
		}
		map=new google.maps.Map($('#map-canvas').get(0),mapSettings);
	}

});