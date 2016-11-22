var Util = {
    htmlDecode: function (input) {
        var e = document.createElement('div');
        e.innerHTML = input;
        return e.childNodes.length === 0 ? "" : e.childNodes[0].nodeValue;
    },
    isEquivalent: function (a, b) {
        // Create arrays of property names
        var aProps = Object.getOwnPropertyNames(a);
        var bProps = Object.getOwnPropertyNames(b);

        // If number of properties is different,
        // objects are not equivalent
        if (aProps.length != bProps.length) {
            return false;
        }

        for (var i = 0; i < aProps.length; i++) {
            var propName = aProps[i];

            // If values of same property are not equal,
            // objects are not equivalent
            if (a[propName] !== b[propName]) {
                return false;
            }
        }

        // If we made it this far, objects
        // are considered equivalent
        return true;
    }
};


function NetworkLoader() {

    var network, edges, myMap, viewEditor;

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
        var defaultIcon = L.icon({
            iconUrl: '/static/leaflet/images/marker-icon.png',
            shadowUrl: '/static/leaflet/images/marker-shadow.png'
        });
        edges.forEach(function (edge) {
            var startNode = edge.start_node,
                endNode = edge.end_node;

            startMarker = new L.marker([startNode.x, startNode.y]);
            if (!nodeExists(nodeSet, startNode)) {
                nodeSet.push(startNode);
                mapNodes.push(startMarker);
                startMarker.addTo(myMap);
                viewEditor.addNodeToList(startMarker);
            }
            endMarker = new L.marker([endNode.x, endNode.y]);
            if (!nodeExists(nodeSet, endNode)) {
                nodeSet.push(endNode);
                mapNodes.push(endMarker);
                endMarker.addTo(myMap);
                viewEditor.addNodeToList(endMarker);
            }

            viewEditor.addEdge(myMap, startMarker, endMarker, defaultIcon);
        });
    }

    function loadMap() {
        readData();
        setNetworkDetails();
        addEdgesToMap();
    }

    return {
        init: function (vEditor) {
            setViewEditor(vEditor);
        },
        loadMap: function (myMap) {
            setMap(myMap);
            loadMap();
        }
    }
}
