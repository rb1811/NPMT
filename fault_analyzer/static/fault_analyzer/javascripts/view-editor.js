function ViewEditor() {
    var faultRegionPolygon;

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
    function deleteFaultNodesFromMap() {
        $('#specified-faults-table').find('tbody').children().find('.delete-node').trigger('click');
    }

    function setNetworkDetails(name, description) {
        $('.network-name').text(name);
        $('.network-description').text(description);
    }

    function addEdge(myMap, startNode, endNode) {
        if (startNode != endNode) {
            var latlngs = [
                [startNode.getLatLng().lat, startNode.getLatLng().lng],
                [endNode.getLatLng().lat, endNode.getLatLng().lng]
            ];
            var polyline = L.polyline(latlngs, {color: 'orange'});
            polyline.addTo(myMap);
        }
    }

    function addNodeToTable(node) {
        var $specifiedFaultsTable = $('#specified-faults-table');
        var view = {
            lat: node.getLatLng().lat,
            lng: node.getLatLng().lng
        }, hoverIcon = L.icon({
            iconUrl: '/static/network_editor/leaflet/images/marker-icon-yellow.png',
            shadowUrl: '/static/network_editor/leaflet/images/marker-shadow.png'
        }), faultIcon = L.icon({
            iconUrl: '/static/network_editor/leaflet/images/marker-icon-red.png',
            shadowUrl: '/static/network_editor/leaflet/images/marker-shadow.png'
        });
        var output = Mustache.render(fault_analyzer.templates.faultNode, view);
        var faultRowEl = $(output);

        faultRowEl.hover(function () {
            node.setIcon(hoverIcon);
        }, function () {
            node.setIcon(faultIcon);
        });

        faultRowEl.find('.delete-node').on('click', function (e) {
            node.remove();
            $(this).parents('tr').remove();
        });

        $specifiedFaultsTable.find('tbody').append(faultRowEl);
    }

    function plotFaultRegion(myMap, nodes) {
        if (faultRegionPolygon) {
            faultRegionPolygon.remove();
        }
        var latlngs = [];
        Array.from(nodes).forEach(function (node) {
            latlngs.push([node.lat, node.lng]);
        });
        faultRegionPolygon = L.polygon(latlngs, {color: 'red'}).addTo(myMap);
    }

    return {
        createNetworkTable: createNetworkTable,
        setNetworkDetails: setNetworkDetails,
        addEdge: addEdge,
        addNodeToTable: addNodeToTable,
        plotFaultRegion: plotFaultRegion,
        deleteFaultNodesFromMap: deleteFaultNodesFromMap
    }
}