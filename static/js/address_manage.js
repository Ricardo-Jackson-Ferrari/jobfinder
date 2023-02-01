let $table = $('#table')

$.getJSON("json/address_data.json")
    .done(function (jsonFromFile) {
        $table.bootstrapTable({ data: jsonFromFile.rows })
    })

let $button_remove = $('#close')

$(function () {
    $button_remove.click(function () {
        let ids = $.map($table.bootstrapTable('getSelections'), function (row) {
            return row.id
        })
        $table.bootstrapTable('remove', {
            field: 'id',
            values: ids
        })
    })
})

function closeFormatter(value, row) {
    return `<button class="close-btn btn-clean" title="Encerrar">
    <i class="fa fa-ban"></i>
    </button>`
}

function addressFormatter(value) {
    return `${value.street}, ${value.number} - ${value.district}, ${value.city} - ${value.uf}, ${value.cep}`
}

function editFormatter(value, row) {
    return `<button class="btn-clean btn-yellow edit" title="Encerrar">
    <i class="fa fa-edit"></i>
    </button>`
}

function viewFormatter(value) {
    viewURL = 'job/manager/show/'
    return `<button class="view btn-clean" title="Visualizar">
      <i class="fa fa-eye"></i>
    </button>`
}

window.operateEvents = {
    'click .close-btn': function (e, value, row, index) {
        let confirmed = confirm(`Tem certeza de que deseja encerrar a vaga "${row.title}" ?`)
        if (confirmed) {
            $table.bootstrapTable('remove', {
                field: 'id',
                values: [row.id]
            })
        }
    },
    'click .edit': function (e, value, row, index) {
        $('#modal_form_address').find('form').trigger('reset')

        $('#modal_form_address').find('input[name="title"]').val(row.title)
        $('#modal_form_address').find('input[name="cep"]').val(row.address.cep)
        $('#modal_form_address').find('input[name="uf"]').val(row.address.uf)
        $('#modal_form_address').find('input[name="city"]').val(row.address.city)
        $('#modal_form_address').find('input[name="district"]').val(row.address.district)
        $('#modal_form_address').find('input[name="street"]').val(row.address.street)
        $('#modal_form_address').find('input[name="number"]').val(row.address.number)
        $('#modal_form_address').find('input[name="complement"]').val(row.address.complement)

        $('#modal_form_address').modal('show')
    }
}

function show_form_add_address() {
    $('#modal_form_address').find('form').trigger('reset')
    $('#modal_form_address').modal('show')
}