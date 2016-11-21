function NetworkEditor() {
    var modes = {add_node: 1, add_edge: 2};
    var myMap, newMarker, markerLocation;
    var mode = modes.add_node;
    var edgeStartNodeAlreadySet = false;
    var startIcon = null;
    var defaultIcon = null;

    var nodeTemplate = network_editor.templates.node;

    function showNodeDetail(popup, newMarker) {
        popup.setLatLng(newMarker.getLatLng())
            .setContent(getNodeTemplate(newMarker.getLatLng()))
            .openOn(myMap);
    }

    function addEdgeToList(start, end, edge) {
        var $edgeLsit = $('.edge-list');
        var view = {
            startLat: start.getLatLng().lat,
            startLng: start.getLatLng().lng,
            endLat: end.getLatLng().lat,
            endLng: end.getLatLng().lng
        };
        var output = Mustache.render(network_editor.templates.edge, view);
        var edgeEl = $(output);
        edgeEl.find('.delete-edge').on('click', function (e) {
            edge.remove();
            $(this).parent('li').remove();
        });
        $edgeLsit.append(edgeEl);
    }

    function addEdge(startNode, newMarker) {
        edgeStartNodeAlreadySet = false;
        startNode.setIcon(defaultIcon);
        if (startNode != newMarker) {
            var latlngs = [
                [startNode.getLatLng().lat, startNode.getLatLng().lng],
                [newMarker.getLatLng().lat, newMarker.getLatLng().lng]
            ];
            var polyline = L.polyline(latlngs, {color: 'red'});
            polyline.addTo(myMap);
            addEdgeToList(startNode, newMarker, polyline);
        }
    }

    function addNodeToList(newMarker) {
        var $nodeLsit = $('.node-list');
        var view = {
            lat: newMarker.getLatLng().lat.toString(),
            lng: newMarker.getLatLng().lng.toString()
        };
        var output = Mustache.render(network_editor.templates.node, view);
        var nodeEl = $(output);
        nodeEl.find('.delete-node').on('click', function (e) {
            newMarker.remove();
            $(this).parent('li').remove();
        });
        $nodeLsit.append(nodeEl);
    }

    var getNetworkDataJson = function () {
        var nodes = [];
        $('.node-list').children().map(function (i, node) {
            nodes.push({lat: $(node).data('lat'), lng: $(node).data('lng')});
        });

        var edges = [];
        $('.edge-list').children().map(function (i, edge) {
            edges.push({
                start: {lat: $(edge).data('startLat'), lng: $(edge).data('startLng')},
                end: {lat: $(edge).data('endLat'), lng: $(edge).data('endLng')}
            });
        });

        var name = $('input.network-name').val();
        var description = $('input.network-description').val();
        return JSON.stringify({
            name: name,
            description: description,
            nodes: nodes,
            edges: edges
        });
    };
    var setupMap = function () {
            myMap = L.map('map').setView([38.487, -75.641], 8);
            var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
            var osmAttrib = 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
            var osm = new L.TileLayer(osmUrl, {minZoom: 0, maxZoom: 18, attribution: osmAttrib});
            myMap.setView(new L.LatLng(33.428242, -111.598434), 5);
            myMap.addLayer(osm);
            startIcon = L.icon({
                iconUrl: '/static/leaflet/images/marker-icon-orange.png',
                shadowUrl: '/static/leaflet/images/marker-shadow.png'
            });
            defaultIcon = L.icon({
                iconUrl: '/static/leaflet/images/marker-icon.png',
                shadowUrl: '/static/leaflet/images/marker-shadow.png'
            });
        },

        getNodeTemplate = function (node) {
            return "<h4>Node Details:</h4>" +
                "<p> Lat: <span > " + node.lat + " </span></p>" +
                "<p> Long: <span >" + node.lng + "  </span ></p>";
        },

        initBindings = function () {
            var addNodeBtn = $('#add-node');
            var addEdgeBtn = $('#add-edge');

            addNodeBtn.on('click', function () {
                mode = modes.add_node;
                addEdgeBtn.removeClass('active');
                addNodeBtn.addClass('active');
            });

            addEdgeBtn.on('click', function () {
                mode = modes.add_edge;
                addEdgeBtn.addClass('active');
                addNodeBtn.removeClass('active');
            });
        },

        setupAddingNodesAndEdges = function () {
            var startNode;
            myMap.on('click', function (e) {
                if (mode == modes.add_node) {
                    var newMarker = new L.marker(e.latlng).addTo(myMap);
                    var popup = L.popup();
                    newMarker.on('click', function (e) {
                        if (mode == modes.add_node) {
                            showNodeDetail(popup, newMarker);
                        } else if (mode == modes.add_edge) {
                            if (edgeStartNodeAlreadySet == false) {
                                edgeStartNodeAlreadySet = true;
                                newMarker.setIcon(startIcon);
                                startNode = newMarker;
                            } else {
                                addEdge(startNode, newMarker);
                            }
                        }
                    });
                    addNodeToList(newMarker);
                }
            });
        },

        bindSave = function () {
            function csrfSafeMethod(method) {
                // these HTTP methods do not require CSRF protection
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }

            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        var csrftoken = Cookies.get('csrftoken');
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            $('#network-form').on('submit', function (e) {
                var url = $(this).data('url');
                var method = $(this).attr('method');

                $.ajax({
                    type: method,
                    url: url,
                    data: getNetworkDataJson(),
                    success: function (data) {
                        console.log("returned successfully: ", data);
                    }
                });

                e.preventDefault();
                return false;
            });
        };
    return {
        initMap: function () {
            setupMap();
            initBindings();
            setupAddingNodesAndEdges();
        },
        setOnSave: function () {
            bindSave();
        }
    }
}


$(function () {
    var networkEditor = new NetworkEditor();
    networkEditor.initMap();
    networkEditor.setOnSave();
});