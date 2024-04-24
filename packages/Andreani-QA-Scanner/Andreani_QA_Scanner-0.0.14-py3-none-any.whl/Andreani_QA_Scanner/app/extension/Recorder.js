let eventCache = null;
let accionsCache = null;
actionsProgressCache = null;
localStorage.setItem('elementContext', JSON.stringify({}));

const searchAllElements = () => {
  /**
   * Activa la busqueda de elementos y le agrega los listener para la captura de los eventos ocurridos sobre ellos.
   * @param {null}.
   * @returns {null}
   **/
  document.addEventListener("mousemove", handleMove, true);
  document.addEventListener("click", handleClick, true);
  document.addEventListener("keydown", handleKeyPress, true);
  document.addEventListener("input", handleInputs, true);

}
handleMove = (event) => {
  /**
  * @param {event} event - evento DOM.
  * @returns {null}
  **/
  if (event.target !== eventCache) {
    let elementContext = buildXpaths(event.target.tagName.toLowerCase(), event.target);
    localStorage.setItem('elementContext', JSON.stringify(elementContext));
    eventCache = event.target;
  }
}

handleClick = () => {
  if (accionsCache !== "Se realizo click en... " + JSON.parse(localStorage.getItem('elementContext'))['XPATH']) {
    accionsCache = "Se realizo click en... " + JSON.parse(localStorage.getItem('elementContext'))['XPATH'];
    highlight(JSON.parse(localStorage.getItem('elementContext'))['XPATH'], "OBJECT");
    let payload = buildResponseBody("click", JSON.parse(localStorage.getItem('elementContext')));
    call_listener_log_events(payload);
  }
  if (actionsProgressCache !== null) {
    let payload = buildResponseBody("input", actionsProgressCache["OBJECT"], actionsProgressCache["VALUE"]);
    call_listener_log_events(payload);
    actionsProgressCache = null;
  }
}

function handleInputs(event) {
  if (checkIsTextInputElement(event.target)) {
    actionsProgressCache = {
      "ACTION": "Escribio",
      "VALUE": (event.target.tagName.toLowerCase() === "div") ? event.target.textContent : event.target.value,
      "OBJECT": buildXpaths(event.target.tagName.toLowerCase(), event.target)
    }
  }
}

checkIsTextInputElement = (element) => {
  // retorna true o false si un elemento es un input element o textarea
  return (
    (element.tagName.toLowerCase() === "input" && ['text', 'password', 'number', 'email', 'tel', 'url', 'search', 'tel'].includes(element.type)) ||
    (element.tagName.toLowerCase() === "div" && ['text', 'password', 'number', 'email', 'tel', 'url', 'search', 'tel'].includes(element.getAttribute("role"))) ||
    (element.tagName.toLowerCase() === "input" && element.getAttribute("role") === undefined) ||
    element.tagName.toLowerCase() === "textarea" ||
    element.isContentEditable
  );
};

// Función para manejar el evento de teclado
function handleKeyPress(event) {
  if (actionsProgressCache !== null) {
    if (event.key === "Enter") {
      highlight(actionsProgressCache["OBJECT"]["XPATH"], "OBJECT");
      let payload = buildResponseBody("input", actionsProgressCache["OBJECT"], actionsProgressCache["VALUE"]);
      call_listener_log_events(payload);
      payload = buildResponseBody("send_key", actionsProgressCache["OBJECT"], "ENTER");
      setTimeout(call_listener_log_events(payload), 100);
      actionsProgressCache = null;
      // Aquí puedes agregar cualquier acción que desees realizar cuando se presione Enter
    }

    // Verificar si se presionó la tecla "Tab"
    if (event.key === "Tab") {
      highlight(actionsProgressCache["OBJECT"]["XPATH"], "OBJECT");
      let payload = buildResponseBody("input", actionsProgressCache["OBJECT"], actionsProgressCache["VALUE"]);
      call_listener_log_events(payload);
      payload = buildResponseBody("send_key", actionsProgressCache["OBJECT"], "TAB");
      setTimeout(call_listener_log_events(payload), 100);
      actionsProgressCache = null;
      // Aquí puedes agregar cualquier acción que desees realizar cuando se presione Tab
    }
  } else {
    if (event.key === "Tab") {
      payload = buildResponseBody("send_key", buildXpaths("html", document.getElementsByTagName("html")[0]), "TAB");
      call_listener_log_events(payload);
    }
    if (event.key === "Enter") {
      payload = buildResponseBody("send_key", buildXpaths("html", document.getElementsByTagName("html")[0]), "ENTER");
      call_listener_log_events(payload);
    }
  }
}

const observerConfigRecord = {
  childList: true,
  subtree: true
};

const observerRecorder = new MutationObserver(searchAllElements);

// Iniciar la observación del DOM con las opciones configuradas
observerRecorder.observe(document, observerConfigRecord);
