function ViewEditor() {
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
        createNetworkTable: createNetworkTable,
        setNetworkDetails: setNetworkDetails
    }
}