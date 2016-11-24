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

    return {
        init: function (vEditor) {
            viewEditor = vEditor;
            initMap();
            // readData();
            // setNetworkDetails();
            bindLoadNetworkModal();
        }

    }
}