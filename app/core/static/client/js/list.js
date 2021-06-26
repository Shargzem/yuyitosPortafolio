var tblClient;
function getData(){
    tblClient =$('#data').DataTable({
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
            {"data": "names"},
            {"data": "surnames"},
            {"data": "rut"},
            {"data": "address"},
            {"data": "gender.name"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#" rel="delete" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}


$(function () {

    modal_title = $('.modal-title');

    getData();

    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Creación de un Cliente');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('form')[0].reset();
        $('#myModalClient').modal('show');
    });


    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        modal_title.find('span').html('Edición de un Cliente');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tblClient.cell($(this).closest('td, li')).index();
        var data = tblClient.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('input[name="names"]').val(data.names);
        $('input[name="surnames"]').val(data.surnames);
        $('input[name="rut"]').val(data.rut);
        $('input[name="address"]').val(data.address);
        $('select[name="gender"]').val(data.gender.id);
        $('#myModalClient').modal('show');
    });

    $('#data tbody').on('click', 'a[rel="delete"]', function () {
        var tr = tblClient.cell($(this).closest('td, li')).index();
        var data = tblClient.row(tr.row).data();
        var parametros =  $(this).serializeArray();
        parametros.push({'name':'action', 'value':'delete'});
        parametros.push({'name':'id', 'value':data.id});
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estás seguro de eliminar este registro ?', parametros, function () {
            tblClient.ajax.reload();
            // getData();
        });
    });





    $('form').on('submit', function (e) {
        e.preventDefault();
        var parametros =  $(this).serializeArray();
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estás seguro de ingresar el siguiente registro ?', parametros, function () {
            $('#myModalClient').modal('hide');
            tblClient.ajax.reload();
            // getData();
        });
    });
});