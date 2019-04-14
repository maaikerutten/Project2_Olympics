var EarthquakesJSON = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson'
console.log (EarthquakesJSON)


function markerSize(magnitude) {
    return magnitude * 4;
};


var earthquakes = new L.LayerGroup();

d3.json(EarthquakesJSON, function (geoJson) {
    L.geoJSON(geoJson.features, {
        pointToLayer: function (geoJsonPoint, latlng) {
            return L.circleMarker(latlng, { radius: markerSize(geoJsonPoint.properties.mag) });
        },

        style: function (geoJsonFeature) {
            return {
                fillColor: Color(geoJsonFeature.properties.mag),
                fillOpacity: 0.7,
                weight: 0.1,
                color: 'black'

            }
        },

        onEachFeature: function (feature, layer) {
            layer.bindPopup(
                "<h4 style='text-align:center;'>" + new Date(feature.properties.time) +
                "</h4> <hr> <h5 style='text-align:center;'>" + feature.properties.title + "</h5>");
        }
    }).addTo(earthquakes);
    createMap(earthquakes);
});

// add colors to earthquakes
function Color(magnitude) {
    if (magnitude > 5) {
        return 'red'
    } else if (magnitude > 4) {
        return 'Orange'
    } else if (magnitude > 3) {
        return 'Yellow'
    } else if (magnitude > 2) {
        return 'Green'
    } else if (magnitude > 1) {
        return 'Blue'
    } else {
        return 'Purple'
    }
};

function createMap() {

    var Map = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.high-contrast',
        accessToken: 'pk.eyJ1IjoicHJvamVjdDEiLCJhIjoiY2p1YzBwbjNnMGpkejQ0cnZ2MDRjMDQ2MCJ9.gfjBLqqtfSyRBupNT6RoAA'
    });

    

    var baseLayers = {
        "Map": Map,
       };

    var overlays = {
        "Earthquakes": earthquakes,
    };

    var mymap = L.map('mymap', {
        center: [40, -99],
        zoom: 4.3,
        timeDimension: true,
        timeDimensionOptions: {
        timeInterval: "2018-04-01/2018-04-05",
        period: "PT1H"
        },
        timeDimensionControl: true,
        layers: [earthquakes]
    });
// NAVRAGEN WAT DIT IS< NODIG VOOR LEVEL 1: 
    L.control.layers(baseLayers, overlays).addTo(mymap);
    L.timeDimension.earthquakes.geoJson(earthquakes).addTo(mymap);
    L.control.timeDimension().addTo(mymap);
    var player = new L.TimeDimension.Player({}, timeDimension).addTo(mymap);

    var tdWmsLayer = L.timeDimension.layer.wms(wmsLayer);
    tdWmsLayer.addTo(map);


// add legend
    var legend = L.control({ position: 'bottomright' });

    legend.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info legend'),
            magnitude = [0, 1, 2, 3, 4, 5],
            labels = [];

        div.innerHTML += "<h4 style='margin:4px'>Magnitude</h4>"

        for (var i = 0; i < magnitude.length; i++) {
            div.innerHTML +=
                '<i style="background:' + Color(magnitude[i] + 1) + '"></i> ' +
                magnitude[i] + (magnitude[i + 1] ? '&ndash;' + magnitude[i + 1] + '<br>' : '+');
        }

        return div;
    };
    legend.addTo(mymap);
}

createMap()