$(document).ready(function(){
    let max_group = 5
	let add_group = $('.add_group')
	let group_wrapper = $('#group-sections')
	let section_wrapper = $('.section_wrapper')

	let max_field = 10
	
	let html_group = `<div class="section_wrapper mt-10">
        <div class="field_wrapper">
            <div class="item mb-10">
                <input type="text" name="section_0_name[0]" class="form-control" placeholder="Sessão"/>
            </div>
        </div>
        <div class="itens">
            <div class="item mb-10">
                <input type="text" name="section_0_item[0]" class="form-control" placeholder="Item"/>
                <a href="javascript:void(0);" class="add_button genric-btn btn-success large" title="Add field"><i class="fa fa-plus"></i></a>
            </div>
        </div>
        <div style="display:flex; justify-content: right;">
        <a href="javascript:void(0);" class="remove_group genric-btn btn-danger large" title="Add section"><i class="fa fa-minus">&nbsp</i>Remover sessão</a>
        </div>
    </div>
            `

	
	let html_fields = `
		<div class="item mb-10">
		    <input type="text" name="section_1_item[]" class="form-control" placeholder="Item"/>
		    <a href="javascript:void(0);" class="remove_button genric-btn btn-danger large"><i class="fa fa-minus"></i></a>
		</div>
        `

	let y = 1
	
    function reNameItens(el) {
        el.children().find('input').each(function(i){
            let section_id = $(this).parent().parent().parent().data('id')
            $(this).attr('name', `section_${section_id}_item[${i}]`)
        })
    }

    function reNameSections(el) {
        el.children().each(function(i){
            $(this).data('id', i)
            reNameItens($(this).closest('.section_wrapper'))
        })
    }
	
	$(add_group).click(function(){
		if( y <= max_group){
			y++
			$(group_wrapper).append(html_group)
            reNameSections(group_wrapper)
		}
	
	})

	$(group_wrapper).on('click', '.remove_group', function(e){
		e.preventDefault()
        $(this).parent().parent(section_wrapper).remove()
		y--
        reNameSections(group_wrapper)
	})


    $('body').on('click','.add_button',function(){
        let count_elements = $(this).closest(".itens").children().length
        if(count_elements < max_field){
            $(this).closest('.itens').append(html_fields)
            reNameItens($(this).closest('.section_wrapper'))
        }
    });

    $('body').on('click', '.remove_button', function(e){
        e.preventDefault()
        let itens = $(this).closest('.section_wrapper')
        $(this).closest('div').remove()
        reNameItens(itens)
    })
})