function NetworkLoader() {

    var network, edges, myMap, viewEditor, nodeEditor, mode;
    var defaultIcon = L.icon({
        iconUrl: '/static/leaflet/images/marker-icon.png',
        shadowUrl: '/static/leaflet/images/marker-shadow.png'
    });

    function readData() {
        var decodedString = Util.htmlDecode(window.network_editor.network);
        network = JSON.parse(decodedString);
        decodedString = Util.htmlDecode(window.network_editor.edges);
        edges = JSON.parse(decodedString);
    }

    function setMap(osmap) {
        myMap = osmap
    }

    function setViewEditor(vEditor) {
        viewEditor = vEditor;
    }

    function setNetworkDetails() {
        viewEditor.setNetworkDetails(network[0].fields.name, network[0].fields.description)
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

    function addEdgesToMap() {
        var nodeSet = [];
        var mapNodes = [];
        var startMarker, endMarker;
        edges.forEach(function (edge) {
            var startNode = edge.start_node,
                endNode = edge.end_node;

            startMarker = new L.marker([startNode.x, startNode.y]);
            if (!nodeExists(nodeSet, startNode)) {
                nodeSet.push(startNode);
                mapNodes.push(startMarker);
                startMarker.addTo(myMap);
                viewEditor.addNodeToList(startMarker);
                nodeEditor.addNode(startMarker);
            }
            endMarker = new L.marker([endNode.x, endNode.y]);
            if (!nodeExists(nodeSet, endNode)) {
                nodeSet.push(endNode);
                mapNodes.push(endMarker);
                endMarker.addTo(myMap);
                viewEditor.addNodeToList(endMarker);
                nodeEditor.addNode(endMarker);
            }

            viewEditor.addEdge(myMap, startMarker, endMarker, defaultIcon);
        });
    }

    function loadMap() {
        readData();
        setNetworkDetails();
        addEdgesToMap();
    }

    function setNodeEditor(nEditor) {
        nodeEditor = nEditor;
    }

    function setNetworkIdData() {
        var href = window.location.pathname;
        var nId = href.substr(href.lastIndexOf('/') + 1);
        $('#network-form').data('id', nId);
    }

    return {
        init: function (vEditor, nEditor) {
            setViewEditor(vEditor);
            setNodeEditor(nEditor);
            setNetworkIdData();
        },
        loadMap: function (myMap) {
            setMap(myMap);
            loadMap();
        }
    }
}
