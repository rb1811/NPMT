var mymap;
var ajaxRequest;
var plotlist;
var plotlayers=[];

function removeMarkers() {
    for (i=0;i<plotlayers.length;i++) {
        mymap.removeLayer(plotlayers[i]);
    }
    plotlayers=[];
}


// then add this as a new function...
function onMapMove(e) { askForPlots(); }

function askForPlots() {
    // request the marker info with AJAX for the current bounds
    var bounds=mymap.getBounds();
    var minll=bounds.getSouthWest();
    var maxll=bounds.getNorthEast();
    var msg='leaflet/findbybbox.cgi?format=leaflet&bbox='+minll.lng+','+minll.lat+','+maxll.lng+','+maxll.lat;
    ajaxRequest.onreadystatechange = stateChanged;
    ajaxRequest.open('GET', msg, true);
    ajaxRequest.send(null);
}

function stateChanged() {
    // if AJAX returned a list of markers, add them to the map
    if (ajaxRequest.readyState==4) {
        //use the info here that was returned
        if (ajaxRequest.status==200) {
            plotlist=eval("(" + ajaxRequest.responseText + ")");
            removeMarkers();
            for (i=0;i<plotlist.length;i++) {
                var plotll = new L.LatLng(plotlist[i].lat,plotlist[i].lon, true);
                var plotmark = new L.Marker(plotll);
                plotmark.data=plotlist[i];
                mymap.addLayer(plotmark);
                plotmark.bindPopup("<h3>"+plotlist[i].name+"</h3>"+plotlist[i].details);
                plotlayers.push(plotmark);
            }
        }
    }
}

function getXmlHttpObject() {
    if (window.XMLHttpRequest) { return new XMLHttpRequest(); }
    if (window.ActiveXObject)  { return new ActiveXObject("Microsoft.XMLHTTP"); }
    return null;
}

function setupMarkers(mymap) {
    // set up AJAX request
    ajaxRequest=getXmlHttpObject();
    if (ajaxRequest==null) {
        alert ("This browser does not support HTTP Request");
        return;
    }

    askForPlots();
    mymap.on('moveend', onMapMove);
}


function initmap() {
    // set up the map
    mymap = new L.Map('map');

    // create the tile layer with correct attribution
    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    var osm = new L.TileLayer(osmUrl, {minZoom: 0, maxZoom: 18, attribution: osmAttrib});
    var marker = new L.marker([33.5, -111.9]).addTo(mymap);
    var marker = new L.marker([33.5, -110.9]).addTo(mymap);
    var marker = new L.marker([34.07029, -111.42883]).addTo(mymap);
    // start the map in South-East England
    mymap.setView(new L.LatLng(33.428242, -111.598434),8);
    mymap.addLayer(osm);

    var circle = L.circle([33.47699, -111.78314], {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 25000
    }).addTo(mymap);

    setupMarkers(mymap);

    var popup = L.popup();

    function onMapClick(e) {
        var m = window.MercatorConverter.ll2m(e.latlng.lng, e.latlng.lat);
        var str = "mercator co ordinates: \nx: " + m.x + " y: " + m.y;
        popup
            .setLatLng(e.latlng)
            .setContent("You clicked the map at " + e.latlng.toString() + " and " + str)
            .openOn(mymap);
    }

    var polygon = L.polygon([
        [33.5, -111.9],
        [33.5, -110.9],
        [34.07029, -111.42883]
    ]).addTo(mymap);


    var polygon = L.polygon([
        [33.5, -111.9],
        [32.69429, -111.09375]
    ]).addTo(mymap);


    mymap.on('click', onMapClick);


}

