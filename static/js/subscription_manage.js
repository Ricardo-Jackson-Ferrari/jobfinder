let $table = $('#table')

function responseHandler(res) {
  let json = {
    total: res.count,
    rows: res.results,
  }
  return json
}


function created_atFormatter(value) {
    let date = new Date(value).toLocaleString('pt-BR')
    return date
}

function viewFormatter(value, row) {
  return `<a href="${row.url}" class="view" target="blank">
            <i class="fas fa-external-link-alt"></i>
          </a>`
}

function claimFormatter(value) {
  return formatMoney(value)
}

function statusFormatter(value) {
  if(value){
    return '<span class="badge badge-success fz-0">Ativa</span>'
  }
  return '<span class="badge badge-danger fz-0">Encerrada</span>'
}

function formatMoney(value) {
  return Intl.NumberFormat('pt-br', { style: 'currency', currency: 'BRL' }).format(value)
}

document.querySelector('.cv-view').addEventListener('click', ()=>{
  $('#modal_pdf').modal('show')
})
