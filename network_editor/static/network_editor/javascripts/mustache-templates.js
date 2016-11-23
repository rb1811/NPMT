window.network_editor = window.network_editor ? window.network_editor : {};
window.network_editor.templates = {
    node: '<li data-lat="{{lat}}" data-lng="{{lng}}" class="list-group-item node-list-item clearfix">' +
    '<p>Lat: <span class="node-lat text-overflow">{{lat}}</span></p>' +
    '<p>Long: <span class="node-lng text-overflow">{{lng}}</span></p>' +
    '<input type="button" value="Delete" class="btn btn-xs btn-danger delete-node pull-right"/> ' +
    "<button type='button' class='edit-node btn btn-xs btn-default'  data-trigger='focus' data-container='body' " +
    "data-toggle='popover'" +
    "data-placement='right' data-html='true' title='Edit node' " +
    "data-content=\"<div class='row'><div class='col-xs-12'>" +
    "<label for='edit-lat'>lat: <input name='edit-lat' class='edit-lat' type='text' value=''></label>" +
    "</div><div class='col-xs-12'>" +
    "<label for='edit-lng'>lng: <input name='edit-lat' class='edit-lng' type='text' value=''></label></div>" +
    "<div class='col-xs-12 text-center'>" +
    "<button class='update-node' class='center btn btn-sm btn-default'>update</button>" +
    "</div>" +
    "</div>\">" +
    "edit" +
    "</button>" +
    '</li>',

    edge: '<li data-start-lat="{{startLat}}" data-start-lng="{{startLng}}" ' +
    'data-end-lat="{{endLat}}" data-end-lng="{{endLng}}"' +
    'class="list-group-item edge-list-item clearfix">' +
    '<p class="edge-start">Start: (<span class="text-overflow">{{startLat}}</span>,<span class="text-overflow">{{startLng}}</span>)</p>' +
    '<p class="edge-end">End: (<span class="text-overflow">{{endLat}}</span>, <span class="text-overflow">{{endLng}}</span>)</p>' +
    '<input type="button" value="Delete" class="btn btn-xs btn-danger delete-edge pull-right"> ' +
    '</li>',

    network: '<tr>' +
    '<th scope="row">{{index}}</th>' +
    '<td>{{name}}</td>' +
    '<td>{{description}}</td>' +
    '<td><a href="{{url}}{{id}}">Load</a></td>' +
    '</tr>'
};