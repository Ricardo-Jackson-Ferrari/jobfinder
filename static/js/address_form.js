document.querySelector('input[name="cep"]').addEventListener('change', (e) => {
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
                document.querySelector('input[name="uf"]').value = data.uf
                document.querySelector('input[name="city"]').value = data.localidade
                document.querySelector('input[name="district"]').value = data.bairro
                document.querySelector('input[name="street"]').value = data.logradouro
            })
    }
})

document.querySelector('#form_address').addEventListener('submit', (e) => {
    e.preventDefault()
})