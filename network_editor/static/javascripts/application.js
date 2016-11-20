function NetworkEditor() {
    var modes = {add_node: 1, add_edge: 2};
    var myMap, newMarker, markerLocation;
    var mode = modes.add_node;
    var setupMap = function () {
            myMap = L.map('map').setView([38.487, -75.641], 8);
            var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
            var osmAttrib = 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
            var osm = new L.TileLayer(osmUrl, {minZoom: 0, maxZoom: 18, attribution: osmAttrib});
            myMap.setView(new L.LatLng(33.428242, -111.598434), 5);
            myMap.addLayer(osm);
        },

        getNodeTemplate = function (node) {
            return "<h4>Node Details:</h4>" +
                "<p> Lat: <span > " + node.lat + " </span></p>" +
                "<p> Long: <span >" + node.lng + "  </span ></p>";
        },

        initBindings = function () {
            var addNodeBtn = $('#add-node');
            addNodeBtn.on('click', function () {
                mode = modes.add_node;
            });

            var addEdgeBtn = $('#add-edge');
            addEdgeBtn.on('click', function () {
                mode = modes.add_edge;
            });
        },

        setupAddingNodes = function () {
            myMap.on('click', function (e) {
                if (mode == modes.add_node) {
                    var newMarker = new L.marker(e.latlng).addTo(myMap);
                    var popup = L.popup();
                    newMarker.on('click', function (e) {
                        if (mode == modes.add_node) {
                            popup.setLatLng(newMarker.getLatLng())
                                .setContent(getNodeTemplate(newMarker.getLatLng()))
                                .openOn(myMap);
                        }
                    });
                }
            });
        };
    return {
        initMap: function () {
            setupMap();
            initBindings();
            setupAddingNodes();
        }
    }
}


$(function () {
    var networkEditor = new NetworkEditor();
    networkEditor.initMap();
});