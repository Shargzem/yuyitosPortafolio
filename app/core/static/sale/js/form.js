var tblProducts;
var vents = {
    items: {
        cli: '',
        date_joined: '',
        subtotal: 0,
        iva: 0.00,
        total: 0,
        products: []
    },
    calculate_invoice: function(){
        var subtotal = 0;
        var iva = $('input[name="iva"]').val();
        $.each(this.items.products, function (pos, dict) {
            dict.pos = pos;
            dict.subtotal = dict.cant * dict.price_sale;
            subtotal+= dict.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * iva;
        this.items.total = this.items.subtotal +  this.items.iva;

        $('input[name="subtotal"]').val(this.items.subtotal);
        $('input[name="ivacalc"]').val(this.items.iva);
        $('input[name="total"]').val(this.items.total);
    },

    add: function(item){
        this.items.products.push(item);
        this.list();
    },

    list: function () {
        this.calculate_invoice();

        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns: [
                {"data": "id"},
                {"data": "name"},
                {"data": "cate.name"},
                {"data": "price_sale"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white"><i class="fas fa-trash-alt"></i></a>';

                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$'+(data);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control  input-sm" autocomplete="off" value="'+data +'">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$'+(data);
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex){
                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 1000000000,
                    step: 1
                });
            },
            initComplete: function (settings, json) {

            }
        });
    },

};

$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    $('#date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });

    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change', function () {
        vents.calculate_invoice();
    })
        .val(0.00);

    // search clients

    $('select[name="cli"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_clients'
                };
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese un cliente',
        minimumInputLength: 1,
    });

    $('.btnAddClient').on('click', function () {
        $('#myModalClient').modal('show');
    });

    $('#myModalClient').on('hidden.bs.modal', function (e) {
        $('#frmClient').trigger('reset');
    });



    $('#frmClient').on('submit', function (e) {
        e.preventDefault();

        var parameters = new FormData(this);
        parameters.append('action', 'create_client');
        //console.log(vents.items);
        //console.log(parametros);
        submit_with_ajax2(window.location.pathname, 'Notificación', '¿Estás seguro de ingresar el cliente ?', parameters, function (response) {
            $('#myModalClient').modal('hide');
        });

    });


    //busqueda de productos

    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname, //window.location.pathname
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 300,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            //console.clear();
            ui.item.cant = 1;
            ui.item.subtotal = 0;
            console.log(vents.items);
            vents.add(ui.item);
            $(this).val('');
        }
    });

    //evento cantidad

    $('.btnRemoveAll').on('click', function () {
        if (vents.items.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            vents.items.products = [];
            vents.list();
        }, function () {

        });


    });

    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?', function () {
                vents.items.products.splice(tr.row, 1);
                vents.list();
            }, function () {

            });
        })
        .on('change ', 'input[name="cant"]', function () {
            console.clear();
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            //console.log(tr);
            vents.items.products[tr.row].cant = cant;
            vents.calculate_invoice();
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal);
        });

    $('.btnClrearSearch').on('click', function () {
        $('input[name=search]').val('').focus();
    });

    // submit

    $('#frmSale').on('submit', function (e) {
        e.preventDefault();

        if(vents.items.products.length === 0){
            mensaje_error('Debe ingresar al menos un producto para procesar la venta');
            return false;
        }

        vents.items.date_joined = $('input[name="date_joined"]').val();
        vents.items.cli = $('select[name="cli"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));
        //console.log(vents.items);
        //console.log(parametros);
        submit_with_ajax2(window.location.pathname, 'Notificación', '¿Estás seguro de ingresar el siguiente registro ?', parameters, function (response) {
            alert_action('Notificación', '¿Deasea imprimir la boleta de venta?', function () {
                window.open('/erp/sale/invoice/pdf/'+ response.id +'/', '_blank');
                location.href = '/erp/sale/list/';
            }, function () {
                location.href = '/erp/sale/list/';
            });

        });

    });

    vents.list();

});