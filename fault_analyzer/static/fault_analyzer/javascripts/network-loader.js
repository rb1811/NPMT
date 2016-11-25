function NetworkLoader() {
    var network, nodes, edges, myMap, viewEditor;

    function initMap() {
        myMap = L.map('map');
        var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
        var osmAttrib = 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
        var osm = new L.TileLayer(osmUrl, {minZoom: 0, maxZoom: 18, attribution: osmAttrib});
        myMap.setView(new L.LatLng(30, 0), 2);
        myMap.addLayer(osm);
    }

    function readData() {
        var decodedString = Util.htmlDecode(window.network_editor.network);
        network = JSON.parse(decodedString);
        decodedString = Util.htmlDecode(window.network_editor.edges);
        edges = JSON.parse(decodedString);
        decodedString = Util.htmlDecode(window.network_editor.nodes);
        nodes = JSON.parse(decodedString);
    }

    function setNetworkDetails() {
        viewEditor.setNetworkDetails(network[0].fields.name, network[0].fields.description)
    }

    function bindLoadNetworkModal() {
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
    }

    function nodeExists(nodeSet, currentNode) {
        var returnVal = false;
        nodeSet.forEach(function (node) {
            if (Util.isEquivalent(node, currentNode)) {
                returnVal = true;
            }
        });
        return returnVal;
    }

    function plotEdges() {
        var startMarker, endMarker, nodeSet = [];
        edges.forEach(function (edge) {
            var startNode = edge.start_node,
                endNode = edge.end_node;

            startMarker = new L.marker([startNode.x, startNode.y]);
            if (!nodeExists(nodeSet, startNode)) {
                nodeSet.push(startNode);
                startMarker.addTo(myMap);
                addNode(startMarker);
            }
            endMarker = new L.marker([endNode.x, endNode.y]);
            if (!nodeExists(nodeSet, endNode)) {
                nodeSet.push(endNode);
                endMarker.addTo(myMap);
                addNode(endMarker);
            }
            viewEditor.addEdge(myMap, startMarker, endMarker);

        });
        return nodeSet;
    }

    function getNodeTemplate(node) {
        return "<h4>Node Details:</h4>" +
            "<p> Lat: <span > " + node.lat + " </span></p>" +
            "<p> Long: <span >" + node.lng + "  </span ></p>";
    }

    function showNodeDetail(popup, nodeMarker) {
        popup.setLatLng(nodeMarker.getLatLng())
            .setContent(getNodeTemplate(nodeMarker.getLatLng()))
            .openOn(myMap);
    }

    function addNode(nodeMarker) {
        var popup = L.popup();
        nodeMarker.on('click', function (e) {
            showNodeDetail(popup, nodeMarker);
        });
    }

    function plotNodes(nodeSet) {
        nodes.forEach(function (node) {
            if (!nodeExists(nodeSet, node)) {
                var nodeMarker = new L.marker([node.x, node.y]);
                nodeMarker.addTo(myMap);
                addNode(nodeMarker);
            }
        });
    }


    function addEdgesAndNodesToMap() {
        var nodeSet = [];
        nodeSet = plotEdges();
        plotNodes(nodeSet);

    }

    function loadNetwork() {
        if (window.network_editor.mode == 'edit') {
            readData();
            setNetworkDetails();
            addEdgesAndNodesToMap();
        }
    }

    return {
        init: function () {
            viewEditor = new ViewEditor();
            initMap();
            bindLoadNetworkModal();
            loadNetwork();
        },
        getMap: function () {
            return myMap;
        }
    }
}