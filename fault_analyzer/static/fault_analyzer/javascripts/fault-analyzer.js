function FaultAnalyzer() {
    var myMap;

    function setupAjaxForCSRF() {
        var csrfSafeMethod = function (method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        };

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    var csrftoken = Cookies.get('csrftoken');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
    }

    function setupFaultTableBindings(faultRadius) {
        var trs = $('table.fault-table').find('tbody tr');
        var circles = new Array(trs);
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

    function setupTrigger() {
        var faultRadius = $('input.fault-radius').val();
        faultRadius = parseInt(faultRadius) * 1000;
        var networkId = window.network_editor.network_id;
        setupAjaxForCSRF();

        $('#analyze-form').on('submit', function (e) {
            var method = $(this).attr('method');
            var url = $(this).data('url');
            $.ajax({
                type: method,
                url: url,
                data: JSON.stringify({network_id: networkId, fault_radius: faultRadius}),
                success: function (data) {
                    if (data.status == 1) {
                        // alert(data.message);
                        setupFaultTableBindings(faultRadius);
                        // console.log(data.results);
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