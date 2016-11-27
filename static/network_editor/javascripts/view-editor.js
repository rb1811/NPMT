function ViewEditor() {

    function addNodeToList(node) {
        var $nodeList = $('.node-list');
        var hoverIcon = L.icon({
            iconUrl: '/static/network_editor/leaflet/images/marker-icon-yellow.png',
            shadowUrl: '/static/network_editor/leaflet/images/marker-shadow.png'
        }), defaultIcon = L.icon({
            iconUrl: '/static/network_editor/leaflet/images/marker-icon.png',
            shadowUrl: '/static/network_editor/leaflet/images/marker-shadow.png'
        });
        var view = {
            lat: node.getLatLng().lat.toString(),
            lng: node.getLatLng().lng.toString()
        };
        var output = Mustache.render(network_editor.templates.node, view);
        var nodeEl = $(output);
        nodeEl.hover(function () {
            node.setIcon(hoverIcon);
        }, function () {
            node.setIcon(defaultIcon);
        });

        var editNode = nodeEl.find('.edit-node');
        editNode.on('shown.bs.popover', function (e) {
            var $editLatInput = $('input.edit-lat');
            var $editLngInput = $('input.edit-lng');
            $editLatInput.val(nodeEl.data('lat'));
            $editLngInput.val(nodeEl.data('lng'));
            $('button.update-node').on('click', function () {
                var latVal = $editLatInput.val();
                var lngVal = $editLngInput.val();
                nodeEl.attr('data-lat', latVal);
                nodeEl.attr('data-lng', lngVal);
                nodeEl.find('.node-lat').text(latVal);
                nodeEl.find('.node-lng').text(lngVal);
                editNode.popover('hide')
                node.setLatLng({lat: latVal, lng: lngVal});
            });
        });
        nodeEl.find('.delete-node').on('click', function (e) {
            node.remove();
            $(this).parent('li').remove();
        });
        $nodeList.append(nodeEl);
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

        edgeEl.hover(function () {
            edge.setStyle({color: 'black'});
        }, function () {
            edge.setStyle({color: 'red'})
        });

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
        var $networks = $('#networks-table');
        $networks.find('tbody').html('');
        networks.forEach(function (network, index) {
            var view = {
                    index: index + 1,
                    id: network.pk,
                    name: network.fields.name,
                    description: network.fields.description,
                    url: $networks.data('url')
                },
                template = network_editor.templates.network;
            var output = Mustache.render(template, view);
            var networkRowEl = $(output);
            $networks.find('tbody').append(networkRowEl);
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