let $table = $('#table')

$.getJSON("json/subscription_data.json")
  .done(function (jsonFromFile) {
    $table.bootstrapTable({ data: jsonFromFile.rows })
  })

function viewFormatter(value) {
  viewURL = 'job/manager/show/'
  return `<button class="view btn-clean" title="Visualizar">
      <i class="fa fa-eye"></i>
    </button>`
}

function claimFormatter(value) {
  return formatMoney(value)
}

function cvFormatter(value) {
  viewURL = 'subscription/manage/view'
  return `<button class="cv-view btn-clean" title="Visualizar">
      <i class="fas fa-file-alt"></i>
    </button>`
}

function formatMoney(value) {
  return Intl.NumberFormat('pt-br', { style: 'currency', currency: 'BRL' }).format(value)
}

window.operateEvents = {
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
    $('#exampleModalLong').find('.modal-body').html(modal_body_div)
    $('#exampleModalLong').modal('show')
  },
  'click .cv-view': function (e, value, row, index) {
    let directory = 'files'
    $('#modal_pdf').find('embed').attr('src', `${directory}/${value}`)
    $('#modal_pdf').modal('show')
  }
}