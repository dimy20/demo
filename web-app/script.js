function rand_int(min, max) {
    return Math.floor(Math.random() * (Math.floor(max) - Math.ceil(min) + 1)) + Math.ceil(min);
}

const init_websocket_connection = () => {
    let socket;
    //const WS_ENDPOINT = "ws://vigilant-ai-api:80/api/stream";

    socket = new WebSocket("ws://127.0.0.1:80/api/stream");
    //socket = new WebSocket("ws://vigilant-ai-api:80/api/stream");

    socket.onopen = (ev) => {
        console.log("Connected!");
    }

    socket.onmessage = function(ev) {
        const chatBody = document.getElementById('chat-body');
        const bot_msg = ev.data;
        // Mensaje de respuesta del bot (puedes personalizar la lógica de la respuesta del bot aquí)
        const botMessageElement = document.createElement('div');
        botMessageElement.classList.add('message', 'bot-message');
        botMessageElement.innerHTML = `<p>${bot_msg}</p>`;
        chatBody.appendChild(botMessageElement);
    };

    socket.onclose = function(ev) {
        console.log('WebSocket is closed now.');
    };

    socket.onerror = (error) => {
        console.error('WebSocket error:', error);
    }

    return socket;
}

const build_calendar = () => {
    const calendar = document.getElementById('calendar');

    const samples = ["level-1", "level-2", "level-2","level-3", "level-3"];
    let values = [];
    for(let i = 0; i < 20; i++){
        let j = rand_int(0, samples.length - 1);
        values.push(samples[j]);
    }
    // Generate 365 cells
    for (let i = 0; i < 371; i++) {
        const cell = document.createElement('div');
        cell.classList.add('cell');

        const index = rand_int(0, values.length-1);
        cell.classList.add(values[index]);
        calendar.appendChild(cell);
    }
}

const save_session_from_url = ()=>{
    const url = window.location.href.split("/")
    const session_id  = url[url.length-1];
    localStorage.setItem("session_id", session_id);
}

document.addEventListener("DOMContentLoaded", function () {
    save_session_from_url();
    build_calendar();
    const socket = init_websocket_connection();
    let btn = document.getElementById("send-message-button");

    btn.addEventListener("click", async () => {
        const input = document.getElementById('chat-input');
        const chatBody = document.getElementById('chat-body');
        const message = input.value.trim();

        if (message) {
            // Mensaje del usuario
            const userMessageElement = document.createElement('div');
            userMessageElement.classList.add('message', 'user-message');
            userMessageElement.innerHTML = `<p>${message}</p>`;
            chatBody.appendChild(userMessageElement);

            const session_id = localStorage.getItem("session_id");

            if(socket.readyState == WebSocket.OPEN){
                console.log("Sending weboskcet messages");
                socket.send(message);
            }

            const response = await fetch("/api/chat/message", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user: "enzo",
                    prompt: message,
                    session_id: session_id
                })
            });

            const data = await response.json();
            console.log(data);

            // Mensaje de respuesta del bot (puedes personalizar la lógica de la respuesta del bot aquí)
            const botMessageElement = document.createElement('div');
            botMessageElement.classList.add('message', 'bot-message');
            botMessageElement.innerHTML = `<p>${data.message}</p>`;
            chatBody.appendChild(botMessageElement);

            // Limpiar el input y hacer scroll hacia abajo
            input.value = '';
            chatBody.scrollTop = chatBody.scrollHeight;
        }

    });

});

function removeChatItem(element) {
    const item = element.parentElement;
    item.remove();
}

