let form_address = document.querySelector('#form_address')

document.querySelector('.btn-add').addEventListener('click', () => {
    form_address.reset()
    $('#exampleModalLong').modal('show')
})