function SpecifiedFaultAnalyzer() {
    var myMap, viewEditor, modes = {
        specified_faults: 'specified_faults',
        generic_faults: 'generic_faults'
    }, faultIcon = L.icon({
        iconUrl: '/static/network_editor/leaflet/images/marker-icon-red.png',
        shadowUrl: '/static/network_editor/leaflet/images/marker-shadow.png'
    }), mode = modes.generic_faults;

    function getNodeTemplate(node) {
        return "<h4>Node Details:</h4>" +
            "<p> Lat: <span > " + node.lat + " </span></p>" +
            "<p> Long: <span >" + node.lng + "  </span ></p>";
    }

    function showNodeDetail(popup, newMarker) {
        popup.setLatLng(newMarker.getLatLng())
            .setContent(getNodeTemplate(newMarker.getLatLng()))
            .openOn(myMap);
    }

    function addNode(node) {
        var popup = L.popup();
        node.setIcon(faultIcon);
        node.on('click', function (e) {
            if (mode == modes.specified_faults) {
                showNodeDetail(popup, node);
            }
        });
    }

    function setupAddingFaultsOnMap() {

        var spefiedFaultCollapsible = $('#specified-faults-collapse');
        spefiedFaultCollapsible.on('show.bs.collapse', function (e) {
            mode = modes.specified_faults;
        });

        spefiedFaultCollapsible.on('hide.bs.collapse', function (e) {
            mode = modes.generic_faults;
        });

        myMap.on('click', function (e) {
            if (mode == modes.specified_faults) {
                var newMarker = new L.marker(e.latlng).addTo(myMap);
                viewEditor.addNodeToTable(newMarker);
                addNode(newMarker);
            }
        });
    }

    function updateFaultDetailsList(data) {
        var $faultList = $('.specified-fault-details-list');
        $faultList.find('.number_of_surviving_nodes').text(data.number_of_surviving_nodes);
        $faultList.find('.number_of_surviving_links').text(data.number_of_surviving_links);
        $faultList.find('.number_of_connected_components').text(data.number_of_connected_components);
        $faultList.find('.largest_connected_component_size').text(data.largest_connected_component_size);
        $faultList.find('.smallest_connected_component_size').text(data.smallest_connected_component_size);
    }

    function get_fault_nodes() {
        var faultRows = $('#specified-faults-table').find('tbody').children();
        var response = {nodes: []};
        faultRows.map(function (i, faultRow) {
            response.nodes.push({lat: $(faultRow).data('lat'), lng: $(faultRow).data('lng')});
        });
        return response
    }

    function bindGenerateFaultRegionAction() {
        $('#generate-fault-region-form').on('submit', function (e) {
            var method = $(this).attr('method');
            var url = $(this).data('url');
            $.ajax({
                type: method,
                url: url,
                data: JSON.stringify(get_fault_nodes()),
                success: function (data) {
                    if (data.status == 1) {
                        window.fault_analyzer.fault_nodes = data.nodes;
                        viewEditor.deleteFaultNodesFromMap();
                        viewEditor.plotFaultRegion(myMap, data.nodes);
                    }
                }
            });

            e.preventDefault();
            return false;
        });
    }

    function bindAnalyzeFaultRegionAction() {
        $('#analyze-fault-network-form').on('submit', function (e) {
            var method = $(this).attr('method');
            var url = $(this).data('url');
            $.ajax({
                type: method,
                url: url,
                data: JSON.stringify({
                    network_id: window.network_editor.network_id,
                    fault_nodes: window.fault_analyzer.fault_nodes
                }),
                success: function (data) {
                    if (data.status == 1) {
                        updateFaultDetailsList(data.results);
                    }
                }
            });
            e.preventDefault();
            return false;
        });
    }

    function bindActions() {
        Util.setupAjaxForCSRF();
        bindGenerateFaultRegionAction();
        bindAnalyzeFaultRegionAction();
    }

    return {
        init: function (map) {
            myMap = map;
            setupAddingFaultsOnMap();
            viewEditor = new ViewEditor();
            bindActions();
        }
    }
}