var UI = null
var toggled = false

function createUI_User(params) {
    UI = document.createElement("div")
    
    UI.style.backgroundColor = 'var(--color-schema-3)'
    UI.style.borderRadius = "5px"
    UI.style.opacity = '0'
    UI.classList.add('account_bg')
    UI.style.position = 'fixed'
    UI.style.right = '15px'
    UI.style.top = '80px'
    UI.style.width = '120px'
    UI.style.height = '100px'

    UI.style.zIndex = 1
    let namelabel = document.createElement('h4')
    namelabel.innerText = params.text
    namelabel.style.color = 'white'

    let Logout_button = document.createElement("button")
    Logout_button.innerText = "Log out"
    Logout_button.type = "submit"
    Logout_button.onclick = function() {
        window.location.href = "/logout"
    }
    
    UI.append(namelabel)
    UI.append(Logout_button)
    document.body.append(UI)

    setInterval(() => {
        if (UI.style.opacity < 0.1) {
        UI.style.visibility = 'hidden'
       } else {
        UI.style.visibility = 'visible'
       }
    }, 50);
}

function on_click( ) {
    toggled = !toggled
    var personaluser = document.getElementById('personaluser') 
    if (personaluser) {
        personaluser.style.scale = 0.3
        if (toggled == false) {
            personaluser.style.backgroundColor = ""
            UI.style.opacity = 0
        } else {
            personaluser.style.backgroundColor = "#2fcc9d"
            UI.style.opacity = 1
        }
        setTimeout(function() {
            personaluser.style.scale = 1
        }, 150)
    }
}