document.querySelectorAll('.icon-eye').forEach(icon => {
    icon.addEventListener('click', el => {
        let classes = el.target.getAttribute('class').split(' ')
        let password_input = el.target.parentElement.parentElement.querySelector('input[name*="password"]')
        if (classes.indexOf('fa-eye') == true) {
            password_input.setAttribute('type', 'text')
            classes[classes.indexOf('fa-eye')] = 'fa-eye-slash'
        } else {
            password_input.setAttribute('type', 'password')
            classes[classes.indexOf('fa-eye-slash')] = 'fa-eye'
        }
        el.target.setAttribute('class', classes.join(' '))
    })
})