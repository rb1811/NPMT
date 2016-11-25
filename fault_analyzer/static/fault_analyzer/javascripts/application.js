$(function () {
    var viewEditor = new ViewEditor();
    var networkLoader = new NetworkLoader();
    networkLoader.init(viewEditor);
    networkLoader.loadNetwork();
    var genericFaultAnalyzer = new GenericFaultAnalyzer();
    genericFaultAnalyzer.init(networkLoader.getMap());
    Util.enableTooltip();
});
