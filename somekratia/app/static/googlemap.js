/**
 * Created by katriinaheiskanen on 26/10/15.
 */
function initialize() {
  var myLatlng = new google.maps.LatLng(60.1728365,24.9399135);
  var mapOptions = {
    zoom: 13,
    center: myLatlng
  }
  var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  var marker = new google.maps.Marker({
      position: myLatlng,
      map: map,
      title: 'Location'
  });
}

google.maps.event.addDomListener(window, 'load', initialize);
