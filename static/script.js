function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    let chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `<div>User: ${userInput}</div>`;

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userInput })
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<div>Assistant: ${data.response}</div>`;
    });

    document.getElementById("user-input").value = "";
}
