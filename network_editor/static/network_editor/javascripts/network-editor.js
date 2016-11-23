function NetworkEditor() {
    var modes = {add_node: 1, add_edge: 2};
    var myMap, newMarker, markerLocation;
    var mode = modes.add_node;
    var edgeStartNodeAlreadySet = false;
    var startIcon = null;
    var defaultIcon = null;
    var viewEditor;
    var edgeStartNode;

    function showNodeDetail(popup, newMarker) {
        popup.setLatLng(newMarker.getLatLng())
            .setContent(getNodeTemplate(newMarker.getLatLng()))
            .openOn(myMap);
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
        var id = $('#network-form').data('id');

        name = name == "" ? "temp" : name;
        description = description == "" ? "temp description" : description;

        return JSON.stringify({
            id: id,
            name: name,
            description: description,
            nodes: nodes,
            edges: edges
        });
    };
    var setupMap = function () {
            myMap = L.map('map');
            var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
            var osmAttrib = 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
            var osm = new L.TileLayer(osmUrl, {minZoom: 0, maxZoom: 18, attribution: osmAttrib});
            myMap.setView(new L.LatLng(30, 0), 2);
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

        addNode = function (node) {
            var popup = L.popup();
            node.on('click', function (e) {
                if (mode == modes.add_node) {
                    showNodeDetail(popup, node);
                } else if (mode == modes.add_edge) {
                    if (edgeStartNodeAlreadySet == false) {
                        edgeStartNodeAlreadySet = true;
                        node.setIcon(startIcon);
                        edgeStartNode = node;
                    } else {
                        edgeStartNodeAlreadySet = viewEditor.addEdge(myMap, edgeStartNode, node, defaultIcon);
                    }
                }
            });
        },

        setupAddingNodesAndEdges = function () {
            // var startNode;
            myMap.on('click', function (e) {
                if (mode == modes.add_node) {
                    var newMarker = new L.marker(e.latlng).addTo(myMap);
                    viewEditor.addNodeToList(newMarker);
                    addNode(newMarker);
                }
            });
        },

        bindLoadNetworkModal = function () {
            $('#load-network-modal').on('show.bs.modal', function (e) {
                var url = $(this).data('url');
                $.ajax({
                    type: 'get',
                    url: url,
                    success: function (data) {
                        viewEditor.createNetworkTable(data.networks);
                    }
                });
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

            function getUrl() {
                if (window.network_editor.mode == 'edit') {
                    return $(this).data('update-url');
                } else {
                    return $(this).data('save-url');
                }
            }

            $('#network-form').on('submit', function (e) {
                var method = $(this).attr('method');
                var url = getUrl.call(this);
                $.ajax({
                    type: method,
                    url: url,
                    data: getNetworkDataJson(),
                    success: function (data) {
                        if (data.status == 1) {
                            alert(data.message);
                            window.location = data.redirect_url
                        }
                    }
                });

                e.preventDefault();
                return false;
            });
        };

    function setViewEditor(vEditor) {
        viewEditor = vEditor;
    }

    return {
        initMap: function (viewEditor) {
            setViewEditor(viewEditor);
            setupMap();
            initBindings();
            setupAddingNodesAndEdges();
            bindSave();
            bindLoadNetworkModal();
        },
        getMap: function () {
            return myMap;
        },
        getMode: function () {
            return mode;
        },
        showNodeDetail: showNodeDetail,
        addNode: addNode
    }
}
