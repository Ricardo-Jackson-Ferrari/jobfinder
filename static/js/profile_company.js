let form_address = document.querySelector('#form_address')

document.querySelector('.btn-add').addEventListener('click', () => {
    form_address.reset()
    $('#exampleModalLong').modal('show')
})

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

function refresh() {
    let select = document.querySelector('select[name="address"]')
    let html = `<option value="">---------</option>`

    fetch('/address/api/')
    .then(res => {
        if(!res.ok && res.status != 400){
            throw new Error(res, res.json())
        }
        return res.json()
    })
    .then(data => {
        data.forEach(el => {
            html += `<option value="${el.id}">${el.title}</option>`
        })
        select.innerHTML = html
        $('select').niceSelect('update')
    })
    .catch(err => console.log(err))
}

form_address.addEventListener('submit', (e) => {
    e.preventDefault()
    const form = e.target
    const submit_msg = form.querySelector('.submit-msg')
    const payload = new FormData(form)
    fetch(form.action, {
        method: "POST",
        body: payload,
        headers: {
            "X-CSRFToken": form.querySelector('input[name="csrfmiddlewaretoken"]').value,
        }
    })
    .then(res => {
        if(!res.ok && res.status != 400){
            throw new Error(res, res.json())
        }
        if (res.status == 201){
            let msg = `<div class="alert alert-success mt-10" role="alert">
                    <span>Endereço criado com sucesso!</span>
                </div>`
            submit_msg.innerHTML = msg
            refresh()
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