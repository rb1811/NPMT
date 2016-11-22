window.network_editor = window.network_editor ? window.network_editor : {}
window.network_editor.templates = {
    node: '<li data-lat="{{lat}}" data-lng="{{lng}}" class="list-group-item node-list-item clearfix">' +
    '<p>Lat: <span class="node-lat truncate">{{lat}}</span></p>' +
    '<p>Long: <span class="node-lng truncate">{{lng}}</span></p>' +
    '<input type="button" value="Delete" class="btn btn-xs btn-danger delete-node pull-right"/> ' +
    '</li>',

    edge: '<li data-start-lat="{{startLat}}" data-start-lng="{{startLng}}" ' +
    'data-end-lat="{{endLat}}" data-end-lng="{{endLng}}"' +
    'class="list-group-item edge-list-item clearfix">' +
    '<p class="edge-start">Start: (<span class="truncate">{{startLat}}</span>,<span class="truncate">{{startLng}}</span>)</p>' +
    '<p class="edge-end">End: (<span class="truncate">{{endLat}}</span>, <span class="truncate">{{endLng}}</span>)</p>' +
    '<input type="button" value="Delete" class="btn btn-xs btn-danger delete-edge pull-right"> ' +
    '</li>',

    network: '<tr>' +
    '<th scope="row">{{index}}</th>' +
    '<td>{{name}}</td>' +
    '<td>{{description}}</td>' +
    '<td><input type="radio" name="optionsNetwork" id="network-id-{{id}}" value="{{id}}" checked></td>' +
    '</tr>'
};