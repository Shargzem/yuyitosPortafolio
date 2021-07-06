$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "date_joined"},
            {"data": "date_end"},
            {"data": "total"},
            {"data": "payment"},
            {"data": "state"},
            {"data": "cli.names"},
            {"data": "desc"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        $('form')[0].reset();
        $('#myModalCredited').modal('show');
    });

    $('#date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });



    $('form').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        submit_with_ajax2(window.location.pathname, 'Notificación', '¿Estás seguro de ingresar el siguiente registro ?', parametros, function () {
            location.reload();
        });
    });
});