$(function () {
    var viewEditor = new ViewEditor();
    var networkLoader = new NetworkLoader();
    networkLoader.init(viewEditor);
    networkLoader.loadNetwork();
});
