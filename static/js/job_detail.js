let $table = $('#table')

function responseHandler(res) {
  let json = {
    total: res.count,
    rows: res.results,
  }
  return json
}

function evaluationFormatter(value) {
  let evaluation = document.createElement('button')
  switch (value) {
    case 'Não avaliado':
      evaluation.className = 'button-secondary' 
      evaluation.innerHTML = value
      break;

    case 'Não apto':
      evaluation.className = 'button-error' 
      evaluation.innerHTML = value
      break;
  
    case 'Incerto':
      evaluation.className = 'button-info' 
      evaluation.innerHTML = value
      break;
  
    case 'Apto':
      evaluation.className = 'button-success' 
      evaluation.innerHTML = value
      break;
  
    default:
      break;
  }
  return evaluation.outerHTML
}

function dateFormatter(value) {
  if (value){
    let date = new Date(value).toLocaleString('pt-BR')
    return date
  }
  return 'Não postado'
}

function candidateFormatter(value, row) {
  return `${capfirst(row.candidate.first_name)} ${capfirst(row.candidate.last_name)}`
}

function cvFormatter(value, row) {
  return `<button
            class="view btn-clean"
            onclick="show_modal_cv(${row.id}, '${row.candidate.cv}')"
            title="Visualizar currículo"
          >
            <i class="fas fa-file-alt"></i>
            Visualizar currículo
          </button>`
}

function salaryFormatter(value) {
  if(parseFloat(value) <= 0){
    return 'A combinar'
  }
  return formatMoney(value)
}

function capfirst(text){
  return text[0].toUpperCase() + text.substring(1);
}

function formatMoney(value) {
  return Intl.NumberFormat('pt-br', { style: 'currency', currency: 'BRL' }).format(value)
}

window.operateEvents = {
  'click .del': function (e, value, row, index) {
        let modal = $('#modal_delete')
        modal.attr('data-id', row.id)
        modal.find('.modal-body').html(`<p>Tem certeza de deseja deletar a vaga de título (${row.title}) ?</p>`)
        modal.modal('show')
    }
}

function show_modal_cv(id, pdf_url) {
  $('#modal_pdf').find('embed').attr('src', `${pdf_url}`)
  $('#modal_pdf').attr('data-id', id)
  $('#modal_pdf').modal('show')
}

function show_modal_job() {
  $('#modal_job_detail').modal('show')
}

function refresh() {
  $('#table').bootstrapTable('refresh', $table.attr('data-url'));
}

function application_patch(target){
  let url = '/job/api/application/'
  let evaluation_value = target.dataset.value
  let modal = document.querySelector('#modal_pdf')

  const data = {
    method: "PATCH",
    headers: {
      "X-CSRFToken": modal.dataset.csrf,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({evaluation: evaluation_value})
  }

  fetch(`${url}${modal.dataset.id}/`, data)
  .then(res => {
      if(!res.ok){
          throw new Error(res, res.json())
      }
      refresh()
  })
  .catch(err => {console.log(err)})
}