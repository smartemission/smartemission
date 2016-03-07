$(document).ready(function () {

    // Create Map with layers
    var map = new L.Map('map', {zoom: 12, center: new L.latLng([51.8348, 5.85])});
    var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib = 'Map data <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    var osmTiles = new L.TileLayer(osmUrl, {attribution: osmAttrib});
    map.addLayer(osmTiles);

    // Precompile Handlebars.js Template
    var source = $("#entry-template").html();
    var template = Handlebars.compile(source);


    // Create icon based on feature props and selected state
    function getMarkerIcon(feature, selected) {
        // Default
        var iconUrl = feature.properties['value_stale'] == '0' ? 'locatie-icon.png' : 'locatie-icon-stale.png';

        return new L.icon({
                    iconUrl: selected ? 'locatie-icon-click.png' : iconUrl,
                    iconSize: [24, 41],
                    iconAnchor: [10, 40]
                });
    }

    // URL of the Smart Emission SOS REST API
    var apiUrl = 'http://api.smartemission.nl/sosemu/api/v1';

    // See http://stackoverflow.com/questions/11916780/changing-getjson-to-jsonp
    // Notice the callback=? . This triggers a JSONP call
    var stationsUrl = apiUrl + '/stations?format=json&callback=?';
    var markers = {};
    var oldMarkerId;

    // Split into categories for ease of templating: gasses, meteo and audio
    var gasLabels = 'CO2,CO,NO2,O3,NH3';
    var meteoLabels = 'Temperatuur,Luchtdruk,Luchtvochtigheid';
    var audioLabels = 'Audio Average Value,Average Audio/Noise Level 1-5';

    // First get stations JSON object via REST
    $.getJSON(stationsUrl, function (data) {
        // Callback when getting stations
        var geojson = L.geoJson(data, {
            pointToLayer: function (feature, latlng) {
                // Create and save Marker
                var icon = getMarkerIcon(feature, false);
                var marker = L.marker(latlng, {icon: icon});
                markers[feature.properties.id] = marker;
                return marker;
            }
        }).addTo(map)
            // When station-marker clicked get Timeseries with last value for that Station
            .on('click', function (e) {
                var feature = e.layer.feature;
                var stationId = feature.properties.id;
                var timeseriesUrl = apiUrl + '/timeseries?format=json&station=' + stationId + '&callback=?';

                $.getJSON(timeseriesUrl, function (data) {
                    // See to which category an observation belongs by matching the label
                    var gasses = [];
                    var meteo = [];
                    var audio = [];

                    for (var idx in data) {
                        var component = data[idx];
                        var label = component.parameters.phenomenon.label;

                        // Is it a gas?
                        if (gasLabels.indexOf(label) >= 0) {
                            gasses.push(component);

                            // Is it a meteo?
                        } else if (meteoLabels.indexOf(label) >= 0) {
                            meteo.push(component);

                            // Is it audio?
                        } else if (audioLabels.indexOf(label) >= 0) {
                            // Is it a audio?
                            audio.push(component);

                            if (label == 'Audio/Noise Level 1-5') {
                                component['offset'] = parseInt(component.lastValue.value) * 20 - 10;
                            }
                        }
                    }

                    // Create station data struct: splitting up component categories
                    var stationData = {
                        station: feature,
                        data: {
                            gasses: gasses,
                            meteo: meteo,
                            audio: audio
                        }
                    };

                    // console.log(stationData);

                    var html = template(stationData);

                    // Hier met JQuery
                    var sidebarElm = $("#sidebar");

                    // sidebarElm clear first
                    sidebarElm.empty();
                    sidebarElm.append(html);
                    sidebar.toggle();

                    // Zoom to station and change icon to yellow

                    // Get the Marker
                    var markerClicked = markers[stationId];
                    if (markerClicked) {
                        var icon = getMarkerIcon(feature, true);
                        markerClicked.setIcon(icon);

                        // Reset previous clicked marker if exists
                        if (oldMarkerId) {
                            var oldMarkerClicked = markers[oldMarkerId];
                            icon = getMarkerIcon(oldMarkerClicked.feature, false);
                            oldMarkerClicked.setIcon(icon);
                        }

                        // Save the clicked marker feature id, to reset
                        oldMarkerId = stationId;
                    }

                    // Coordinaten geometrie (lon,lat) en LatLon object (lat, lon) moeten omgedraaid
                    var zoomTo = feature.geometry.coordinates;
                    map.setView(new L.latLng([zoomTo[1], zoomTo[0]]), 17);
                });
            });
    });

    var sidebar = L.control.sidebar('sidebar', {
        closeButton: true,
        position: 'left'
    });
    map.addControl(sidebar);

    map.on('click', function () {
        sidebar.hide();
        map.setView([51.8348, 5.85], 12);
    });

    sidebar.on('show', function () {
        console.log('Sidebar will be visible.');
    });
    sidebar.on('shown', function () {
        console.log('Sidebar is visible.');
    });
    sidebar.on('hide', function () {
        console.log('Sidebar will be hidden.');
    });
    sidebar.on('hidden', function () {
        console.log('Sidebar is hidden.');
    });

    sidebar.on(sidebar.getCloseButton(), 'click', function () {
        console.log('Close button clicked.');
    });

});
