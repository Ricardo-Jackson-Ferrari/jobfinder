let $table = $('#table')

$(function () {
    $('input[name="zipcode"]').mask('00000-000');
})

function closeFormatter(value, row) {
    return `<button class="del danger-btn btn-clean" title="Deletar">
    <i class="fa fa-trash"></i>
    </button>`
}

function addressFormatter(value, row) {
    return `${row.street}, ${row.number} - ${row.district}, ${row.city} - ${row.uf}, ${row.zipcode}`
}

function editFormatter(value, row) {
    return `<button class="btn-clean btn-yellow edit" title="Editar">
    <i class="fa fa-edit"></i>
    </button>`
}

window.operateEvents = {
    'click .del': function (e, value, row, index) {
        let modal = $('#modal_delete')
        modal.attr('data-id', row.id)
        modal.find('.modal-body').html(`<p>Tem certeza de deseja deletar o endereço de título (${row.title}) e endereço ${addressFormatter('', row)}</p>`)
        modal.modal('show')
    },
    'click .edit': function (e, value, row, index) {
        let modal = $('#modal_form_address')

        modal.find('form').trigger('reset')
        modal.find('form').attr('action', `/address/api/${row.id}/`)
        modal.find('form').attr('data-method', 'PATCH')
        modal.find('.submit-msg').html('')

        modal.find('input[name="title"]').val(row.title)
        modal.find('input[name="zipcode"]').val(row.zipcode)
        modal.find('input[name="zipcode"]').trigger('input')
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
    $('#modal_form_address').find('form').attr('action', '/address/api/')
    $('#modal_form_address').find('form').attr('data-method', 'POST')
    $('#modal_form_address').find('.submit-msg').html('')
    $('select').niceSelect('update')
    $('#modal_form_address').modal('show')
}

function refresh() {
    $('#table').bootstrapTable('refresh', '/address/api/');
}


function message_close_modal(text, status) {
    let msg = `<div class="text-center mb-3 message-content">
                            <div class="alert alert-${status ? status : 'success'}" role="alert">
                                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                    <span>&times;</span>
                                </button>
                                ${text}
                            </div>
                    </div>`
    refresh()
    $('.dashboard-content').prepend(msg)
    $('#modal_form_address').modal('hide')
}

document.querySelector('input[name="zipcode"]').addEventListener('change', (e) => {
    if (e.target.value.length == 9) {
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
    const data = {
        method: form.dataset.method,
        body: payload,
    }
    if (form.dataset.method != 'GET'){
        data['headers'] = {
            "X-CSRFToken": form.querySelector('input[name="csrfmiddlewaretoken"]').value
        }
    }
    fetch(form.action, data)
    .then(res => {
        if(!res.ok && res.status != 400){
            throw new Error(res, res.json())
        }
        if (res.status == 201){
            message_close_modal('endereço criado com sucesso!')
        }else if (res.status == 200){
            message_close_modal('endereço atualizado com sucesso!')
            return
        }else{
            return res.json()
        }
    })
    .then(data => {
        if (data){
            let msg = ''
            for (const [key, value] of Object.entries(data)) {
                if(key != 'non_field_errors'){
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
    fetch(`/address/api/${modal.dataset.id}/`, {method: "DELETE", headers: { "X-CSRFToken": modal.dataset.csrf },})
    .then(res => {
        if(!res.ok){
            throw new Error(res, res.json())
        }
        message_close_modal('endereço deletado com sucesso!', 'warning')
    })
    .catch(err => {console.log(err)})
})
