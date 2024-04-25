var select2_widget = function () {

    function initselect2(select_id, ajax, tags, data, placeholder, html_template, html_result_template, selected_ajax, cleared_ajax, keyboard_open) {
        function strip_id(org_id) {
            if (org_id.substring(0, 3) === 'id_') {
                return org_id.substring(3);
            } else {
                return org_id;
            }
        }
        if (html_template === undefined) {
            html_template = function html_template(text) {
                return "<span>" + text.text + "</span>";
            };
        }
        if (html_result_template === undefined) {
            html_result_template = html_template
        }
        var select_element
        if (django_modal.active_modal_container_id() != 'modal-0'){
           select_element = $("#" + select_id, '#' + django_modal.active_modal_container_id());
        } else {
            select_element = $("#" + select_id);
        }
        if (selected_ajax===true) {
            select_element.on('select2:select', function () {
                ajax_helpers.post_json({
                    data: {
                        select2: strip_id(select_id) + '_selected',
                        data: select_element.select2('data')
                    }
                });
            });
        } else if (selected_ajax==='form'){
            select_element.on('select2:select', function () {
                django_modal.send_inputs({select2: strip_id(select_id) + '_selected'})
            });
        }
        if (cleared_ajax===true) {
            select_element.on('select2:clear', function () {
                ajax_helpers.post_json({
                    data: {
                        select2: strip_id(select_id) + '_cleared',
                        data: select_element.select2('data')
                    }
                });
            });
        } else if (cleared_ajax==='form'){
            select_element.on('select2:clear', function () {
                django_modal.send_inputs({select2: strip_id(select_id) + '_cleared'})
            });
        }

        var modal_container = select_element.closest(".modal-content");
        if (modal_container.length === 0) {
            modal_container = $(document.body);
        }
        var modal_url = django_modal.modal_div().attr("data-url");
        var select2_params = {
            theme: "bootstrap4",
            dropdownParent: modal_container,
            allowClear: true,
            placeholder: placeholder
        };

        if (data !== undefined) {
            select2_params.data = data;
        }

        if (data !== undefined || ajax) {
            select2_params.templateSelection = function (text) {
                return $(html_template(text));
            };
            select2_params.templateResult = function (text) {
                return $(html_result_template(text));
            };
            select2_params.escapeMarkup = function (text) {
                return text;
            };
        }

        if (tags.enabled) {
            select2_params.tags = true;
            select2_params.createTag = function (params) {
                var term = $.trim(params.term);
                if (term === "") {
                    return null;
                }
                return {
                    id: tags.new_marker + term,
                    text: term
                };
            };
        }
        if (ajax) {
            select2_params.ajax = {
                method: "POST",
                url: modal_url,
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", ajax_helpers.getCookie("csrftoken"));
                },
                cache: false,
                contentType: "application/json",
                data: function (params) {
                    var ajax_data = {};
                    var raw_values = {}
                    $($("#" + select_id).closest("form")).serializeArray().map(function (x) {
                        ajax_data[x.name] = x.value;
                        if(!raw_values.hasOwnProperty(x.name)) {
                            raw_values[x.name] = [x.value];
                        } else {
                            raw_values[x.name].push(x.value)
                        }
                    });
                    ajax_data.raw_values = raw_values;
                    ajax_data.select2 = strip_id(select_id);
                    ajax_data.search = params.term;
                    ajax_data.page = params.page || 1;
                    return JSON.stringify(ajax_data);
                }
            };
        }
        select_element.select2(select2_params);
        $(".select2-selection__rendered").hover(function () {
            $(this).removeAttr("title");
        });
        if (keyboard_open) {
            $('.select2-selection', select_element.next()).keydown((ev) => {
                if (ev.which < 32)
                    return;
                var target = jQuery(ev.target).closest('.select2-container');
                if (!target.length)
                    return;
                target = target.prev();
                target.select2('open');
                var search = target.data('select2').dropdown.$search ||
                    target.data('select2').selection.$search;
                search.focus();
            });
        }
    }
    return {
        initselect2: initselect2,
    };
}();
