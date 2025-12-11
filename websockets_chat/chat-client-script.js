
function find_id(id) {
    return document.getElementById(id)
}
_message_input = find_id("message-input")
_send_button = find_id("send-button")
_chat_log = find_id("chat-log")
_nickname_input = find_id("nickname-input")
_nickname_ok = find_id("nickname-ok")
_error_overlay = find_id("error-alert")

// Show message on the chat
function display_message(message) {
    msg_json = JSON.parse(message)

    _message = document.createElement("div")
    _content = document.createElement("span")
    _message.classList.add("message")
    _content.classList.add("content")
    _content.innerHTML = msg_json.Message

    if (msg_json.Sender) {
        _sender = document.createElement("span")
        _sender.classList.add("sender")
        _sender.innerHTML = msg_json.Sender;
        _message.appendChild(_sender)
    }

    if (msg_json.Type == "server-msg") {
        _message.classList.add("from-server")
    }

    _message.appendChild(_content)
    _chat_log.appendChild(_message)
}

// Connect
HOST = "localhost"
PORT = 55555
socket = null
chosen_nickname = ""

function socket_connect() {
    socket = new WebSocket(`ws://${HOST}:${PORT}`)

    socket.addEventListener("open", () => {
        msg_connect = { Nick: chosen_nickname }
        socket.send(JSON.stringify(msg_connect))
        console.log(`Connecting as ${chosen_nickname}`)
        hide_nickname_input()
    })

    socket.addEventListener("message", (event) => {
        console.log(`Message received: ${event.data}`)
        display_message(event.data)
    })

    socket.addEventListener("error", (event) => {
        _error_overlay.classList.remove("hidden")
        _nickname_ok.value = "Connect"
        _nickname_ok.disabled = false
    })
}

function socket_send(message) {
    socket.send(message)
}

function hide_nickname_input() {
    _select_nick = document.querySelectorAll("#joining-overlay, #joining-overlay *")
    for (let i = 0; i < _select_nick.length; i++) {
        _select_nick[i].classList.add("hidden")
    }
}

// Submit nickname
_nickname_ok.addEventListener("click", (event) => {
    chosen_nickname = _nickname_input.value
    socket_connect()
    _nickname_ok.value = "Connecting..."
    _nickname_ok.disabled = true
})

_nickname_input.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        event.preventDefault()
        _nickname_ok.click()
    }
})

// Submit message
_send_button.addEventListener("click", () => {
    if (_message_input.value != "") {
        socket_send(_message_input.value)
        _message_input.value = ""
    }
})

_message_input.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        event.preventDefault()
        _send_button.click()
    }
})