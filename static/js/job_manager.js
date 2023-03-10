let $table = $('#table')
let xd

function responseHandler(res) {
  let json = {
    total: res.count,
    rows: res.results,
  }
  return json
}

function statusFormatter(value, row) {
  if(!value){
    return 'Inativo'
  }
  let html = `<div class="d-flex justify-content-center align-items-center">
      <span>Ativo</span>
      <button class="danger-btn btn-clean position-absolute" style="right:0;" title="Encerrar" onclick="modal_close(${row.id}, '${row.title}')">
        <i class="fa fa-ban"></i>
      </button>
    </div>`
  return html
}

function posted_atFormatter(value) {
  if (value){
    let date = new Date(value).toLocaleString('pt-BR')
    return date
  }
  return 'Não postado'
}

function closeFormatter(value, row) {
  if (!row.status) {
    return `<button class="del danger-btn btn-clean" title="Deletar">
        <i class="fa fa-trash"></i>
      </button>`
  }
}

function viewFormatter() {
  return `<button class="view btn-clean" title="Visualizar">
      <i class="fa fa-eye"></i>
    </button>`
}

function salaryFormatter(value) {
  if(parseFloat(value) <= 0){
    return 'A combinar'
  }
  return formatMoney(value)
}

function detailFormatter(value, row) {
  return `<a href="/account/company/job/${row.id}/" class="view"><i class="fas fa-plus"></i></a>`
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
          <p>${row.status ? 'Ativo' : 'Inativo'}</p>
      </div>`
    modal_body_div.innerHTML += status

    let address = `<div class="post-details1 mb-10">
          <div class="small-section-tittle">
              <h4>Local</h4>
          </div>
          <p>${row.address == null ? 'Não especificado' : row.address}</p>
      </div>`
    modal_body_div.innerHTML += address

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
          <p>${row.modality}</p>
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

function modal_close(id, title) {
  let modal = $('#modal_close')
  modal.attr('data-id', id)
  modal.find('.modal-body').html(`<p>Tem certeza de deseja encerrar a vaga de título (${title}) ?</p>`)
  modal.modal('show')
}

function show_modal_cv(pdf_url) {
  let directory = 'files'
  $('#modal_pdf').find('embed').attr('src', `${directory}/${pdf_url}`)
  $('#modal_pdf').modal('show')
}

function show_modal_add_job() {
  $('#modal_job_create').find('form').trigger('reset')
  $('#modal_job_create').find('form').find('#group-sections').html('')
  $('#modal_job_create').modal('show')
}


function refresh() {
  $('#table').bootstrapTable('refresh', '/job/api/');
}

function message_close_modal(modal, text, status) {
  let msg = `<div class="text-center mb-3 message-content">
                    <div class="alert alert-${status ? status : 'success'}" role="alert">
                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span>&times;</span>
                        </button>
                        ${text}
                    </div>
            </div>`
  refresh()
  $('#div-messages').html(msg)
  modal.modal('hide')
}

$(document).ready(function(){
  let aux_group = 0
  let max_group = 5
  let max_field = 5
  let add_group = $('.add_group')
  let group_wrapper = $('#group-sections')
  let section_wrapper = $('.section-wrapper')

  group_wrapper.sortable({
    group: 'no-drop',
    handle: 'i.fa-arrows-alt',
    onDragStart: function ($item, container, _super) {
      if(!container.options.drop)
        $item.clone().insertAfter($item);
      _super($item, container);
    }
  })

  function html_group(section_number) {
    return `<div class="section-wrapper mt-10" data-section-number="${section_number}" >
              <div class="d-flex justify-content-between mb-10 align-items-center">
              <i class="fas fa-arrows-alt" title="Mover"></i>
              <button type="button" href="javascript:void(0);" class="remove_group genric-btn button button-error" title="Remove seção"><i class="fa fa-minus">&nbsp</i>Remover seção</button>
              </div>
              <div class="field_wrapper">
                  <div class="item mb-10">
                      <input type="text" name="sections[${section_number}].title" class="form-control" required placeholder="Seção"/>
                  </div>
              </div>
              <div class="itens mb-10" data-count-itens="1">
                  <div class="item mb-10 align-items-center">
                      <i class="fas fa-arrows-alt" title="Mover"></i>
                      <input type="text" name="sections[${section_number}].itens[0].item" class="form-control" placeholder="Item" required/>
                      <button type="button" class="remove_button button button-error" title="Remover item"><i class="fa fa-minus"></i></button>
                  </div>
              </div>
              <div class="text-center">
              <button type="button" class="add_row button button-info" title="Adicionar item"><i class="fa fa-plus">&nbsp;</i>Adicionar item</button>
              </div>
              <div style="display:flex; justify-content: right;">
              
              </div>
          </div>
        `
  }


  function html_fields(section_number, item_number) {
    return `<div class="item mb-10 align-items-center">
              <i class="fas fa-arrows-alt"></i>
              <input type="text" name="sections[${section_number}].itens[${item_number}].item" class="form-control" required placeholder="Item"/>
              <button type="button" class="remove_button button button-error" title="Remover item"><i class="fa fa-minus"></i></button>
          </div>
        `
  }


  let y = 1

  $(add_group).click(function(){
    if( y <= max_group){
      y++
      let html = $(html_group(aux_group))
      html.find('.itens').sortable({
        group: 'no-drop',
        handle: 'i.fa-arrows-alt',
        onDragStart: function ($item, container, _super) {
          if(!container.options.drop)
            $item.clone().insertAfter($item);
          _super($item, container);
        }
      })
      $(group_wrapper).append(html)
      aux_group++
    }

  })

  $(group_wrapper).on('click', '.remove_group', function(e){
    e.preventDefault()
        $(this).parent().parent(section_wrapper).remove()
    y--
  })

  $('body').on('click','.add_row',function(){
      let count_elements = $(this).closest('.section-wrapper').find(".itens").children().length
      if(count_elements < max_field){
        let current_section_number = $(this).parent().parent().data('section-number')
        
        let list_itens = $(this).parent().parent().find('.itens')
        let current_item_number = list_itens.data('count-itens')
        list_itens.data('count-itens', list_itens.data('count-itens')+1)

        list_itens.append(html_fields(current_section_number, current_item_number))
      }
  });

  $('body').on('click', '.remove_button', function(e){
      e.preventDefault()
      $(this).closest('div').remove()
  })
})
let errors

document.querySelector('#form_job').addEventListener('submit', (e) => {
  e.preventDefault()
  const form = e.target
  const modal = $(`#${e.target.id}`).closest('.modal')
  
  const submit_msg = form.querySelector('.submit-msg')
  const payload = form2js(form, '.', true)
  const data = {
      method: form.dataset.method,
      body: JSON.stringify(payload),
  }
  if (form.dataset.method != 'GET'){
      data['headers'] = {
        "Content-Type": "application/json; charset=UTF-8",
        "X-CSRFToken": form.dataset.csrftoken
      }
  }
  fetch(form.action, data)
  .then(res => {
      if(!res.ok && res.status != 400){
          throw new Error(res, res.json())
      }
      if (res.status == 201){
          message_close_modal(modal, 'vaga criada com sucesso!')
      }else{
          return res.json()
      }
  })
  .then(data => {
      if (data){
          let msg = ''
          errors = data
          for (const [key, value] of Object.entries(data)) {
              if(key != 'non_field_errors'){
                if (key == 'sections') {
                  for(const [field, error] of value){
                    msg += `<div class="alert alert-warning mt-10" role="alert">
                                <span>${key}:${error}</span>
                            </div>`
                  }
                }else{
                  msg += `<div class="alert alert-warning mt-10" role="alert">
                              <span>${key}:${value}</span>
                          </div>`
                }
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

document.querySelector('#btn_delete_job').addEventListener('click', e=>{
  let modal = document.querySelector('#modal_delete')
  const modal_jquery = $(`#${e.target.id}`).closest('.modal')
  fetch(`/job/api/${modal.dataset.id}/`, {method: "DELETE", headers: { "X-CSRFToken": modal.dataset.csrf },})
  .then(res => {
      if(!res.ok){
          throw new Error(res, res.json())
      }
      message_close_modal(modal_jquery, 'vaga deletada com sucesso!', 'warning')
  })
  .catch(err => {console.log(err)})
})

document.querySelector('#btn_close_job').addEventListener('click', e=>{
  let modal = document.querySelector('#modal_close')
  const modal_jquery = $(`#${e.target.id}`).closest('.modal')
  fetch(`/job/api/${modal.dataset.id}/`, {method: "PATCH", headers: { "X-CSRFToken": modal.dataset.csrf },})
  .then(res => {
      if(!res.ok){
          throw new Error(res, res.json())
      }
      message_close_modal(modal_jquery, 'vaga encerrada com sucesso!')
  })
  .catch(err => {console.log(err)})
})
