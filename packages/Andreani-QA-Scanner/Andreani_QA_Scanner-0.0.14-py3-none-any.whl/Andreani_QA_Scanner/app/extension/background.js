chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === "fetchAPI") {
    fetch('https://ejemplo.com/api/datos')
      .then(response => {
        if (!response.ok) {
          throw new Error('La solicitud no fue exitosa');
        }
        return response.json();
      })
      .then(data => {
        // Enviar datos de vuelta al content.js
        sendResponse(data);
      })
      .catch(error => {
        console.error('Error al realizar la solicitud:', error);
      });

    // Devolver true para indicar que sendResponse será llamado asincrónicamente
    return true;
  }
});