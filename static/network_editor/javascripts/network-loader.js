function NetworkLoader() {

    var network, nodes, edges, myMap, viewEditor, nodeEditor, mode;
    var defaultIcon = L.icon({
        iconUrl: '/static/network_editor/leaflet/images/marker-icon.png',
        shadowUrl: '/static/network_editor/leaflet/images/marker-shadow.png'
    });

    function readData() {
        var decodedString = Util.htmlDecode(window.network_editor.network);
        network = JSON.parse(decodedString);
        decodedString = Util.htmlDecode(window.network_editor.edges);
        edges = JSON.parse(decodedString);
        decodedString = Util.htmlDecode(window.network_editor.nodes);
        nodes = JSON.parse(decodedString);
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

    function plotEdges() {
        var startMarker, endMarker, nodeSet = [];
        edges.forEach(function (edge) {
            var startNode = edge.start_node,
                endNode = edge.end_node;

            startMarker = new L.marker([startNode.x, startNode.y]);
            if (!nodeExists(nodeSet, startNode)) {
                nodeSet.push(startNode);
                startMarker.addTo(myMap);
                viewEditor.addNodeToList(startMarker);
                nodeEditor.addNode(startMarker);
            }
            endMarker = new L.marker([endNode.x, endNode.y]);
            if (!nodeExists(nodeSet, endNode)) {
                nodeSet.push(endNode);
                endMarker.addTo(myMap);
                viewEditor.addNodeToList(endMarker);
                nodeEditor.addNode(endMarker);
            }
            viewEditor.addEdge(myMap, startMarker, endMarker, defaultIcon);

        });
        return nodeSet;
    }

    function plotNodes(nodeSet) {
        nodes.forEach(function (node) {
            if (!nodeExists(nodeSet, node)) {
                var nodeMarker = new L.marker([node.x, node.y]);
                nodeMarker.addTo(myMap);
                viewEditor.addNodeToList(nodeMarker);
                nodeEditor.addNode(nodeMarker);
            }
        });
    }

    function addEdgesAndNodesToMap() {
        var nodeSet = [];
        nodeSet = plotEdges();
        plotNodes(nodeSet);
    }

    function loadMap() {
        readData();
        setNetworkDetails();
        addEdgesAndNodesToMap();
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
