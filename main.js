// Replace with your actual WebSocket endpoint
let socket = new WebSocket("wss://oceanotech.in/chat");
// let socket = new WebSocket("ws://localhost:8000");

socket.onopen = () => {
    console.log("Connected to server");
    addMessage("Connected to chat server", "system");
    socket.send("Hello from client JS!");
};

socket.onmessage = (event) => {
    addMessage(event.data, "server");
};

socket.onclose = () => {
    addMessage("Disconnected from server", "system");
};

function sendMessage() {
    const input = document.getElementById("msg");
    const msg = input.value.trim();
    if (!msg) return;

    socket.send(msg);
    addMessage("You: " + msg, "me");
    input.value = "";
}

function addMessage(text, sender) {
    const msgList = document.getElementById("messages");
    const li = document.createElement("li");
    li.textContent = text;

    if (sender === "me") li.classList.add("me");
    else if (sender === "server") li.classList.add("server");

    msgList.appendChild(li);
    msgList.scrollTop = msgList.scrollHeight; // Auto scroll to bottom
}
