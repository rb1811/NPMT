function FaultAnalyzer() {
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
                        alert(data.message);
                        console.log(data.results);
                    }
                }
            });

            e.preventDefault();
            return false;
        });
    }

    return {
        init: function () {
            setupTrigger();
        }
    }
}