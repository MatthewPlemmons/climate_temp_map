
var map;

var info = new google.maps.InfoWindow();

// Initialize map
$(function() {

    var styles = [
        {
            featureType: "all",
            elementType: "labels",
            stylers: [
                {visibility: "off"}
            ]
        }
    ];

    var options = {
        center: {lat: 38.904, lng: -77.016},
        disableDefaultUI: true,
        styles: styles,
        zoom: 12,
    }

    var canvas = $('#map').get(0);

    map = new google.maps.Map(canvas, options);

    google.maps.event.addListenerOnce(map, "idle", configure);
});

// EMILY IS AWESOME

function configure()
{

    // configure typeahead
    $('#q').typeahead({
        highlight: true,
        minLength: 1
    },
    {
        limit: 10,
        source: find_cities,
        templates: {
            empty: "no cities found yet",
            suggestion: _.template("<p> <%- place_name %>, <%- admin_code1 %> (<%- postal_code %>) </p>")
        }
    });

    // centers map on the city selected from typeahead
   $('#q').on("typeahead:selected", function(eventObject, suggestion, name) {

        var latitude = (_.isNumber(suggestion.latitude)) ? suggestion.latitude : parseFloat(suggestion.latitude);
        var longitude = (_.isNumber(suggestion.longitude)) ? suggestion.longitude : parseFloat(suggestion.longitude);

        map.setCenter({lat: latitude, lng: longitude});

        find_nearest_station(suggestion);
    });

    // text box will have the input focus
    $('#q').focus();
}

// Returns cities to typeahead based on user input
function find_cities(query, cb)
{
    var parameters = {
        geo: query
    };
    $.getJSON("search", parameters)
    .done(function(data, textStatus, jqXHR) {
        
        console.log(data);
        cb(data);

    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        console.log(errorThrown.toString());
    });

}

// Shows an Info Window with details about the city
function showInfoWindow(selected_city, marker)
{
    // Maybe write a server function that
    // retrieves and returns some data from Wikipedia.
    var div = "<div id='info'>";
    div += selected_city.place_name + ", " + selected_city.admin_code1;
    div += "</div>";

    info.setContent(div);
    info.open(map, marker);

}

// Locates the closest weather stations to the city selected by the user.
function find_nearest_station(selected_city)
{    
    // add a clear marker function here as well.
    addMarker(selected_city);

    var parameters = {
        lat: selected_city.latitude,
        lng: selected_city.longitude
    };
    $.getJSON("station", parameters)
    .done(function(data, textStatus, jqXHR) {
        
        
        console.log(data);

    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        console.log(errorThrown.toString());
    });

}

function addMarker(location)
{
    var latLng = new google.maps.LatLng(location['latitude'], location['longitude']);

    var marker = new MarkerWithLabel({
        position: latLng,
        draggable: false,
        map: map,
        labelConent: location['place_name'] + ", " + location['admin_code1'],
        labelAnchor: new google.maps.Point(30, 0),
        labelClass: "labels",
    })

    showInfoWindow(location, marker);

}





