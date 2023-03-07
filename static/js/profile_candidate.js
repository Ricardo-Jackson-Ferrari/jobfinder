function update_preview_cv(event){
    if(event.target.files.length > 0){
        let src = URL.createObjectURL(event.target.files[0])
        $('#modal_pdf').find('embed').attr('src', src)
    }
}

function show_cv(){
    $('#modal_pdf').modal('show')
}
