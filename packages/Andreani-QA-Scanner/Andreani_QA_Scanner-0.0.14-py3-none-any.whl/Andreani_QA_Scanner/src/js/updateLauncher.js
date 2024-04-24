async function refreshMessage(message) {
  // Actualiza el string del objeto 'messageLog'
  const messageContainer = document.getElementById("messageLog");
  let opacity = 1;
  while (opacity > 0) {
    messageContainer.style.opacity = opacity;
    await wait(50);
    opacity -= 0.15;
  }
  messageContainer.textContent = message;
  opacity = 0;
  while (opacity < 1) {
    messageContainer.style.opacity = opacity;
    await wait(50);
    opacity += 0.15;
  }
}

function wait(ms) {
  // realiza una espera.
  return new Promise((resolve) => setTimeout(resolve, ms));
}