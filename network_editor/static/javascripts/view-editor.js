function ViewEditor() {

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

    function addEdge(myMap, startNode, endNode, defaultIcon) {
        var edgeStartNodeAlreadySet = false;
        startNode.setIcon(defaultIcon);
        if (startNode != endNode) {
            var latlngs = [
                [startNode.getLatLng().lat, startNode.getLatLng().lng],
                [endNode.getLatLng().lat, endNode.getLatLng().lng]
            ];
            var polyline = L.polyline(latlngs, {color: 'red'});
            polyline.addTo(myMap);
            addEdgeToList(startNode, endNode, polyline);
        }
        return edgeStartNodeAlreadySet;
    }

    function createNetworkTable(networks) {
        networks.forEach(function (network, index) {
            var view = {
                    index: index + 1,
                    id: network.pk,
                    name: network.fields.name,
                    description: network.fields.description
                },
                template = network_editor.templates.network;
            var output = Mustache.render(template, view);
            var networkRowEl = $(output);
            $('#networks-table').find('tbody').append(networkRowEl);
        });
    }

    function setNetworkDetails(name, description) {
        $('.network-name').val(name);
        $('.network-description').val(description);
    }
    return {
        addNodeToList: addNodeToList,
        createNetworkTable: createNetworkTable,
        addEdge: addEdge,
        setNetworkDetails: setNetworkDetails
    }
}