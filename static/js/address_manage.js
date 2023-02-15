let $table = $('#table')

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

function addressFormatter(value, row) {
    return `${row.street}, ${row.number} - ${row.district}, ${row.city} - ${row.uf}, ${row.zipcode}`
}

function editFormatter(value, row) {
    return `<button class="btn-clean btn-yellow edit" title="Encerrar">
    <i class="fa fa-edit"></i>
    </button>`
}

window.operateEvents = {
    'click .close-btn': function (e, value, row, index) {
        let modal = $('#modal_delete')
        modal.attr('data-id', row.id)
        modal.find('.modal-body').html(`<p>Tem certeza de deseja deletar o endereço de título (${row.title}) e endereço ${addressFormatter('', row)}</p>`)
        modal.modal('show')
    },
    'click .edit': function (e, value, row, index) {
        let modal = $('#modal_form_address')

        modal.find('form').trigger('reset')
        modal.find('form').attr('action', `/address/update/${row.id}/`)
        modal.find('.submit-msg').html('')

        modal.find('input[name="title"]').val(row.title)
        modal.find('input[name="zipcode"]').val(row.zipcode)
        modal.find('select[name="uf"]').val(row.uf)
        modal.find('input[name="city"]').val(row.city)
        modal.find('input[name="district"]').val(row.district)
        modal.find('input[name="street"]').val(row.street)
        modal.find('input[name="number"]').val(row.number)
        modal.find('input[name="complement"]').val(row.complement)
        $('select').niceSelect('update')
        modal.modal('show')
    }
}

function show_form_add_address() {
    $('#modal_form_address').find('form').trigger('reset')
    $('#modal_form_address').find('form').attr('action', '/address/create/')
    $('#modal_form_address').find('.submit-msg').html('')
    $('select').niceSelect('update')
    $('#modal_form_address').modal('show')
}

function refresh() {
    $('#table').bootstrapTable('refresh', '/address/list');
}

document.querySelector('input[name="zipcode"]').addEventListener('change', (e) => {
    if (e.target.value.length == 8) {
        fetch(`https://viacep.com.br/ws/${e.target.value}/json/`)
            .then(resp => {
                if (resp.ok) {
                    return resp.json()
                }
            })
            .then(data => {
                if (data.erro) {
                    throw new Error('Cep inválido')
                }
                document.querySelector('select[name="uf"]').value = data.uf
                document.querySelector('input[name="city"]').value = data.localidade
                document.querySelector('input[name="district"]').value = data.bairro
                document.querySelector('input[name="street"]').value = data.logradouro
                $('select').niceSelect('update')
                document.querySelector('input[name="number"]').focus()
            })
    }
})

document.querySelector('#form_address').addEventListener('submit', (e) => {
    e.preventDefault()
    const form = e.target
    const submit_msg = form.querySelector('.submit-msg')
    const payload = new FormData(form)
    fetch(form.action, {
        method: "POST",
        body: payload,
    })
    .then(res => {
        if(!res.ok && res.status != 400){
            throw new Error(res, res.json())
        }
        return res.json()
    })
    .then(data => {
        if (data.status_code == 201 || data.status_code == 200){
            let msg = `<div class="alert alert-success mt-10" role="alert">
                    <span>${data.message}</span>
                </div>`
            submit_msg.innerHTML = msg
            refresh()
        }else{
            let msg = `<div class="alert alert-danger mt-10" role="alert">
                            <span>${data.message}</span>
                        </div>`
            for (const [key, value] of Object.entries(data.errors)) {
                if(key != '__all__'){
                    msg += `<div class="alert alert-warning mt-10" role="alert">
                                <span>${key}:${value}</span>
                            </div>`
                }else{
                    msg += `<div class="alert alert-warning mt-10" role="alert">
                                <span>${value}</span>
                            </div>`
                }
            }
            submit_msg.innerHTML = msg
        }
    })
    .catch(err => console.log(err))
})

document.querySelector('#btn_delete_address').addEventListener('click', e=>{
    let modal = document.querySelector('#modal_delete')
    fetch(`/address/delete/${modal.dataset.id}/`, {method: "POST", headers: { "X-CSRFToken": modal.dataset.csrf },})
    .then(res => {
        if(!res.ok){
            throw new Error(res, res.json())
        }
        return res.json()
    })
    .then(data => {
        refresh()
    })
    .catch(err => {console.log(err)})
})
