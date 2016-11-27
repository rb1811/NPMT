$(function () {
    var viewEditor = new ViewEditor();
    var networkEditor = new NetworkEditor();
    networkEditor.initMap(viewEditor);

    if (window.network_editor.mode == 'edit') {
        var networkLoader = new NetworkLoader();
        networkLoader.init(viewEditor, networkEditor);
        networkLoader.loadMap(networkEditor.getMap());
    }
    Util.enablePopover();
});