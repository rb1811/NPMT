$(function () {

    var networkLoader = new NetworkLoader();
    networkLoader.init();
    // networkLoader.loadNetwork();

    var genericFaultAnalyzer = new GenericFaultAnalyzer();
    genericFaultAnalyzer.init(networkLoader.getMap());

    var specifiedFaultAnalyzer = new SpecifiedFaultAnalyzer();
    specifiedFaultAnalyzer.init(networkLoader.getMap());

    Util.enableTooltip();
});
