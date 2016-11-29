function GenericFaultAnalyzer() {
    var myMap, circles;

    function setupFaultTableBindings(faultRadius) {
        var trs = $('table.fault-table').find('tbody tr');
        circles = new Array(trs);
        trs.toArray().forEach(function (tr, i) {
            $(tr).on('click', function () {
                var self = $(this);
                if (self.attr('data-selected') == 'true') {
                    self.attr('data-selected', 'false');
                    circles[i].remove();
                } else {
                    self.attr('data-selected', 'true');
                    var lat = self.find(".lat").text(),
                        lng = self.find(".lng").text();
                    circles[i] = new L.circle([lat, lng], {radius: faultRadius}).addTo(myMap);
                }
            });
        });
    }

    function updateRBCDNFaultTable(rbcdn_faults) {
        var $faultTable = $('table.fault-table');
        $faultTable.find('tbody').html('');
        rbcdn_faults.forEach(function (fault, index) {
            var view = {
                index: index + 1,
                lat: fault.x,
                lng: fault.y
            };
            var template = fault_analyzer.templates.rbcdn_fault_row;
            var output = Mustache.render(template, view);
            var faultTableRowEl = $(output);
            $faultTable.find('tbody').append(faultTableRowEl);
        });
    }

    function updateFaultDetailsList(data) {
        var $faultList = $('.fault-details-list');
        $faultList.find('.composition_deposition_number').text(data.composition_deposition_number);
        $faultList.find('.largest_component_size').text(data.largest_component_size);
        $faultList.find('.smallest_component_size').text(data.smallest_component_size);
        $faultList.find('.fault_regions_considered').text(data.fault_regions_considered);
    }

    function setupTrigger() {
        var networkId = window.network_editor.network_id;
        Util.setupAjaxForCSRF();

        $('#analyze-form').on('submit', function (e) {
            // circles.forEach(function (circle) {
            //    circle.remove();
            // });
            var method = $(this).attr('method');
            var url = $(this).data('url');
            var faultRadius = $('input.fault-radius').val();
            faultRadius = parseInt(faultRadius) * 1000;
            $.ajax({
                type: method,
                url: url,
                data: JSON.stringify({network_id: networkId, fault_radius: faultRadius}),
                success: function (data) {
                    if (data.status == 1) {
                        // alert(data.mes  sage);
                        updateRBCDNFaultTable(data.results.rbcdn_faults);
                        setupFaultTableBindings(faultRadius);
                        updateFaultDetailsList(data.results);
                    }
                }
            });

            e.preventDefault();
            return false;
        });
    }

    return {
        init: function (map) {
            myMap = map;
            setupTrigger();
        }
    }
}