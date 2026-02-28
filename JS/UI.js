function Create_UI(Purpose, inputs=['name'], path) {
    var ui = document.createElement('div')
    ui.id = 'ui'
    ui.style.position = 'fixed'
    ui.style.top = '50svh'
    ui.style.left = '50svw'
    ui.style.transform = 'translate(-50%, -50%)'
    ui.style.backgroundColor = 'rgba(44, 44, 44, 0.88)'
    ui.style.color = 'white'
    ui.style.padding = '20px'
    ui.style.borderRadius = '10px'
    ui.style.zIndex = '10000'
    ui.style.fontFamily = 'Arial, sans-serif'
    ui.style.textAlign = 'center'
    

    var bg = document.createElement('div')
    bg.id = 'ui-bg'
    bg.style.position = 'fixed'
    bg.style.top = '0'
    bg.style.left = '0'
    bg.style.width = '100vw'
    bg.style.height = '100vh'
    bg.style.backgroundColor = 'rgba(0, 0, 0, 0.5)'
    bg.style.zIndex = '9999'
    bg.onclick = function() {
        document.body.removeChild(ui)
        document.body.removeChild(bg)
    }
    document.body.appendChild(bg)

    var title = document.createElement('h2')
    title.innerText = 'Create for ' + Purpose
    ui.appendChild(title)

    var form = document.createElement('form')
    var inp = document.createElement('input')
    inp.type="hidden"; inp.name="path" ;inp.value=path
    form.append(inp)


    form.onsubmit = function(event) {
        event.preventDefault()
        var formData = {}
        inputs.forEach(function(input) {
            formData[input.name ?? input] = document.getElementById('input-' + input).value
        })
        formData[inp.name] = inp.value

        console.log('Form Data:', formData)

        fetch('/create/'+ Purpose, {
            method: 'POST',
            body: new FormData(form)
        }).then(function(response) {
            if (response.ok) {
                location.reload()
            } else {
                alert('Error creating ' + Purpose)
            }
        })

        document.body.removeChild(ui)
        document.body.removeChild(bg)
    }

    inputs.forEach(function(input) {
        var label = document.createElement('label')
        label.innerText = input.charAt(0).toUpperCase() + input.slice(1) + ': '
        label.htmlFor = 'input-' + input
        form.appendChild(label)

        var inputField = document.createElement('input')
        inputField.type = 'text'
        inputField.id = 'input-' + input
        inputField.name = input
        inputField.required = true
        form.appendChild(inputField)

        form.appendChild(document.createElement('br'))
    })

    var submitButton = document.createElement('button')
    submitButton.type = 'submit'
    submitButton.innerText = 'Submit'
    form.appendChild(submitButton)

    ui.appendChild(form)
    document.body.appendChild(ui)
}

function simpleui(inputs=['name'], purpose, route, types=[]) {
    var class_ = "forminpsettings"
    var ui = document.createElement('div')
    ui.id = 'ui'
    ui.style.position = 'fixed'
    ui.style.top = '50svh'
    ui.style.left = '50svw'
    ui.style.transform = 'translate(-50%, -50%)'
    ui.style.backgroundColor = 'rgba(44, 44, 44, 0.88)'
    ui.style.color = 'white'
    ui.style.padding = '20px'
    ui.style.borderRadius = '10px'
    ui.style.zIndex = '10000'
    ui.style.fontFamily = 'Arial, sans-serif'
    ui.style.textAlign = 'center'
    ui.classList.add(class_)
     var bg = document.createElement('div')
    bg.id = 'ui-bg'
    bg.style.position = 'fixed'
    bg.style.top = '0'
    bg.style.left = '0'
    bg.style.width = '100vw'
    bg.style.height = '100vh'
    bg.style.backgroundColor = 'rgba(0, 0, 0, 0.5)'
    bg.style.zIndex = '9999'
    bg.onclick = function() {
        document.body.removeChild(ui)
        document.body.removeChild(bg)
    }
    document.body.appendChild(bg)
    var form = document.createElement('form')
    var title = document.createElement('h2')
    title.innerText = purpose
    ui.appendChild(title)

    form.onsubmit = function(event) {
        event.preventDefault()
        var formData = {}
        inputs.forEach(function(input) {
            formData[input.name ?? input] = document.getElementById('input-' + input).value
        })

        console.log('Form Data:', formData)

        fetch('/'+(route ?? 'createacc')+"/", {
            method: 'POST',
            body: new FormData(form)
        }).then(function(response) {
            if (response.ok) {
                location.reload()
                alert('Account made sucessfully')
            } else {
                alert('Error creating ' + purpose)
            }
        })

        document.body.removeChild(ui)
        document.body.removeChild(bg)
    }
    form.style.textAlign = "left"
    var loc = 0
    inputs.forEach(function(input) {
        
        var type = "uk"
        console.log(types,loc)
        if (loc in (types ?? [])) {
            type = types[loc]

        }
        
        var label = document.createElement('label')
        label.innerText = input.charAt(0).toUpperCase() + input.slice(1) + ': '
        label.htmlFor = 'input-' + input
        form.appendChild(label)
        let create_br = function(){
            let br = document.createElement('br')
            form.append(br)
            return br
        }
        create_br()
        var inputField = document.createElement('input')
        if (type != "uk") {
            if (type != 'dir') {
                inputField.type = type
            } else {
                inputField.type = 'file'
            }
            if (type == 'file') {
                inputField.multiple = true
                inputField.accept = ".*"
            } else if (type == 'dir') {
                inputField.webkitdirectory = true
                inputField.multiple = true
            }
        } else {
            if (input == 'password') {
        
                inputField.type = 'password'
            } else {
                inputField.type = 'text'
            }
        }
        loc ++
        inputField.classList.add(class_)
        inputField.id = 'input-' + input
        inputField.name = input
        inputField.placeholder = input
        inputField.required = true
        inputField.style.width = "fit-content"
        inputField.style.textAlign = "left"
        form.appendChild(inputField)
        create_br()
        form.appendChild(document.createElement('br'))
    })

    var submitButton = document.createElement('button')
    submitButton.type = 'submit'
    submitButton.innerText = 'Submit'
    form.appendChild(submitButton)

    ui.appendChild(form)
    document.body.appendChild(ui)
}