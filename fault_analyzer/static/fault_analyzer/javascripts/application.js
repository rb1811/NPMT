$(function () {
    var viewEditor = new ViewEditor();
    var networkLoader = new NetworkLoader();
    networkLoader.init(viewEditor);
    networkLoader.loadNetwork();
    var faultAnalyzer = new FaultAnalyzer();
    faultAnalyzer.init(networkLoader.getMap());
});
