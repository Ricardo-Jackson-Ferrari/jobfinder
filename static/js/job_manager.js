let $table = $('#table')

$.getJSON("json/job_data.json")
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
  if (row.status != 'encerrado') {
    return `<button class="close-btn btn-clean" title="Encerrar">
        <i class="fa fa-ban"></i>
      </button>`
  }
}

function viewFormatter() {
  viewURL = 'job/manager/show/'
  return `<button class="view btn-clean" title="Visualizar">
      <i class="fa fa-eye"></i>
    </button>`
}

function copyFormatter(value, row) {
  return `<button class="btn-yellow btn-clean copy" title="Copiar">
      <i class="fa fa-copy"></i>
    </button>`
}

function salaryFormatter(value) {
  return formatMoney(value)
}

function detailFormatter(index, row) {
  let table = document.createElement('table')
  row.subscribeds.forEach(obj => {
    let tr = document.createElement('tr')
    tr.innerHTML = `<td>${obj.name}</td>
      <td>${formatMoney(obj.salary)}</td>
      <td><button class="genric-btn btn-info show_cv" onclick="show_modal_cv('${obj.curriculum}')">Currículo</button></td>`
    table.appendChild(tr)
  })
  return table
}

function formatMoney(value) {
  return Intl.NumberFormat('pt-br', { style: 'currency', currency: 'BRL' }).format(value)
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
  'click .copy': function (e, value, row, index) {
    $('#modal_job_create').find('form').trigger('reset')
    $('#modal_job_create').find('input[name="title"]').val(row.title)
    $('#modal_job_create').find('input[name="vacancies"]').val(row.vacancies)
    $('#modal_job_create').modal('show')
  },
  'click .view': function (e, value, row, index) {

    let modal_body_div = document.createElement('div')
    modal_body_div.setAttribute('class', 'job-post-details')

    let title = `<div class="post-details1 mb-10">
          <div class="small-section-tittle">
              <h4>Título</h4>
          </div>
          <p>${row.title}</p>
      </div>`
    modal_body_div.innerHTML += title

    let status = `<div class="post-details1 mb-10">
          <div class="small-section-tittle">
              <h4>Status</h4>
          </div>
          <p>${row.status}</p>
      </div>`
    modal_body_div.innerHTML += status

    let location = `<div class="post-details1 mb-10">
          <div class="small-section-tittle">
              <h4>Local</h4>
          </div>
          <p>${row.location}</p>
      </div>`
    modal_body_div.innerHTML += location

    let salary = `<div class="post-details1 mb-10">
          <div class="small-section-tittle">
              <h4>Salário</h4>
          </div>
          <p>${formatMoney(row.salary)}</p>
      </div>`
    modal_body_div.innerHTML += salary

    let type = `<div class="post-details1 mb-30">
          <div class="small-section-tittle">
              <h4>Modalidade</h4>
          </div>
          <p>${row.type}</p>
      </div>`
    modal_body_div.innerHTML += type

    let description = `<div class="post-details1 mb-30">
          <div class="small-section-tittle">
              <h4>Descrição</h4>
          </div>
          <p>${row.description}</p>
      </div>`
    modal_body_div.innerHTML += description

    let sections = ''
    if (row.sections) {
      row.sections.forEach(section => {
        let itens = ''
        section.itens.forEach(item => {
          itens += `<li>${item}</li>`
        })
        sections += `<div class="post-details2  mb-30">
            <div class="small-section-tittle">
                <h4>${section.title}</h4>
            </div>
          <ul>
              ${itens}
          </ul>
        </div>`
      })
    }
    modal_body_div.innerHTML += sections
    $('#modal_job_detail').find('.modal-body').html(modal_body_div)
    $('#modal_job_detail').modal('show')
  },
}

function show_modal_cv(pdf_url) {
  let directory = 'files'
  $('#modal_pdf').find('embed').attr('src', `${directory}/${pdf_url}`)
  $('#modal_pdf').modal('show')
}

function show_modal_add_job() {
  $('#modal_job_create').find('form').trigger('reset')
  $('#modal_job_create').modal('show')
}