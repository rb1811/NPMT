window.fault_analyzer = window.fault_analyzer ? window.fault_analyzer : {};
window.fault_analyzer.templates = {

    rbcdn_fault_row: '<tr><th scope="row">{{index}}</th>' +
    '<td><span class="text-overflow lat">{{lat}}</span>' +
    '</td>' +
    '<td><span class="text-overflow lng">{{lng}}</span>' +
    '</td>' +
    '</tr>',

    network: '<tr>' +
    '<th scope="row">{{index}}</th>' +
    '<td>{{name}}</td>' +
    '<td>{{description}}</td>' +
    '<td><a href="{{url}}{{id}}">Load</a></td>' +
    '</tr>',

    faultNode: '<tr data-lat="{{lat}}" data-lng="{{lng}}">' +
    '<th scope="row">&bull;</th>' +
    '<td class="text-overflow lat"><span>{{lat}}</span></td>' +
    '<td class="text-overflow lng"><span>{{lng}}</span></td>' +
    '<td>' +
    '<button type="button" class="delete-node btn btn-danger btn-xs">' +
    'remove' +
    '</button>' +
    '</td>' +
    '</tr>'
};