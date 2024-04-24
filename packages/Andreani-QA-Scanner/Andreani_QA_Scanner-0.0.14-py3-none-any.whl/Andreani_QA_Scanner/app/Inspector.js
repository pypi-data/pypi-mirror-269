window.myScripts = {
  "FRAME": 'MAIN',
  "ELEMENT CONTEXT": null,
  "LOCATOR": false,
  "ACTIVATED": false,
  "CONTROL OVERLAY": 0
};
window.inspectorCalledFrom //variable para identificar desde donde se esta llamando al inspector.js

const style = document.createElement('style');
style.textContent = `
        .myBoxOverlay {
            position: absolute;
            z-index: 99999 !important;
            background-color: #bbdefb;
            opacity: 0.5;
            border-radius: 2px;
            border: 2px dashed #0d47a1;
            cursor: crosshair;
        }`;
document.head.appendChild(style);


const logTargetOnMouseOver = (event) => {
  if (window.myScripts['ACTIVATED']) {
    if (!event.target.classList.contains('myBoxOverlay')) {
      if (window.myScripts['ELEMENT CONTEXT'] !== event.target) {
        cleanOverlay();
        window.myScripts['CONTROL OVERLAY'] = 0;
        window.myScripts['ELEMENT CONTEXT'] = event.target;
        if (window.inspectorCalledFrom !== 'recorder'){
          overlay(event.target);
        }
      }
    }
  }
}

const handleClick = (event) => {
  /**
  * llama a las funciones que realizan la limpieza de las cajas creadas para señalar los objetos, apaga la localizacion y envia al servidor el objeto construido.
  * @param {event} event - evento DOM.
  * @returns {null}
  **/
  cleanOverlay();
  if (window.inspectorCalledFrom !== 'recorder') {
    activateLocationModeOff();
  }
  buildXpaths(window.myScripts['ELEMENT CONTEXT'].tagName.toLowerCase(), window.myScripts['ELEMENT CONTEXT']);
  if (checkIsTextInputElement(window.myScripts['ELEMENT CONTEXT'])) {
    addListenerInputElement(window.myScripts['ELEMENT CONTEXT'])
  }
  call_listener_log_events();
}

const searchAllElements = () => {
  /**
   * Activa la busqueda de elementos y le agrega los listener para la captura de los eventos ocurridos sobre ellos.
   * @param {null}.
   * @returns {null}
   **/

  allElements = document.querySelectorAll('*');
  allElements.forEach(element => {
    element.addEventListener("click", handleClick);
  });

  const myBoxes = document.querySelectorAll('*:not(div.myBoxOverlay)');
  myBoxes.forEach(box => {
    box.addEventListener('mousemove', logTargetOnMouseOver);
  });
  document.addEventListener('mousemove', handleMouseMoveOnElement);
};

const addListenerInputElement = (inputElement) => {
  // agrega event listener blur al elemento input o textarea

  // llamo al back para avisar que se esta escribiendo en un input, para luego mostrarlo en el event logguer
  inputElement.addEventListener('input', () => {
    if (inputElement.value.length === 1) {
      call_listener_log_events('logUserInput');
    }
  })

  inputElement.addEventListener("blur", function () {
    if (inputElement.value) {
      call_listener_log_events(inputElement.value);
    }
  });
};

const checkIsTextInputElement = (element) => {
  // retorna true o false si un elemento es un input element o textarea
  return (
    element.tagName.toLowerCase() === "input" ||
    element.tagName.toLowerCase() === "textarea" ||
    element.isContentEditable
  );
};

const handleMouseMoveOnElement = (event) => {
  /**
  * Controla los eventos de movimiento del mouse para mantener o desactivar los elmentos señalados.
  * @param {event} event - evento DOM.
  * @returns {null}
  **/
  if (window.inspectorCalledFrom !== 'recorder' ){
    console.log(event.target);
  }
  window.myScripts['CONTROL OVERLAY'] = window.myScripts['CONTROL OVERLAY'] + 1;
  if (window.myScripts['CONTROL OVERLAY'] > 10) {
    window.myScripts['ELEMENT CONTEXT'] = '';
    cleanOverlay();
  }
}

const overlay = (elementTarget) => {
  /**
  * Dibuja una caja sobre el elemento con el que se esta interactuando.
  * @param {object} elementTarget - elemento web
  * @returns {null}
  **/
  if (elementTarget) {
    if (elementTarget.tagName !== 'IFRAME') {
      const box = document.createElement('div');
      box.classList.add('myBoxOverlay');
      box.setAttribute('title', elementTarget.tagName);
      const elementTargetRects = elementTarget.getClientRects();
      const elementTargetRect = elementTargetRects[0];
      try {
        box.style.left = `${elementTargetRect.left}px`;
        box.style.top = `${elementTargetRect.top}px`;
        box.style.width = `${elementTargetRect.width}px`;
        box.style.height = `${elementTargetRect.height}px`;
      } catch {
        console.log('No es posible señalar ');
      }
      document.body.appendChild(box);
    }
  }
}

const cleanOverlay = () => {
  /**
  * Elimina las cajas que se utilizaron para señalar los elementos.
  * @param {null}
  * @returns {null}
  **/
  const mybox = document.body.querySelectorAll('div.myBoxOverlay');
  mybox.forEach(myElementBox => {
    myElementBox.remove();
  });
}

const buildResponseBody = (dataToSend) => {
  if (dataToSend === "deleteAllSteps" && window.inspectorCalledFrom === "recorder") {
    // si se llama desde la func para generar una captura de pantalla cuando esta en modo recorder
    return {
      event: "reset recorder steps",
      target: null,
      value: null,
      frame: null,
      location: "recorder",
    };
  }

  if (dataToSend === "screenshot" && window.inspectorCalledFrom === "recorder") {
    // si se llama desde la func para generar una captura de pantalla cuando esta en modo recorder
    return {
      event: "screenshot",
      target: null,
      value: window.urlDomain,
      frame: null,
      location: "recorder",
    };
  }

  if (dataToSend === "urlLog" && window.inspectorCalledFrom === "recorder") {
    // si se llama desde la func para informar cambio de url cuando esta en modo recorder
    return {
      event: "url log",
      target: null,
      value: window.urlDomain,
      frame: null,
      location: "recorder",
    };
  }

  if (dataToSend === "logUserInput" && window.inspectorCalledFrom === "recorder") {
    // si se llama desde la func para informar que un usuario esta escribiendo en un input cuando esta en modo recorder
    return {
      event: "log user input",
      target: window.my_elements[0],
      value: null,
      frame: window.myScripts["FRAME"],
      location: "recorder",
    };
  }

  return {
    // si se llama tanto del recorder con un evento click o input, o si se esta utilizando en modo inspector
    event: dataToSend ? "input" : "click",
    target: window.my_elements[0],
    value: dataToSend ? dataToSend : null,
    frame: window.myScripts["FRAME"],
    location:
      window.inspectorCalledFrom == "recorder" ? "recorder" : "inspector",
  };
};

const call_listener_log_events = (dataToSend = null) => {  // ESTO ESTA MUERTO !!!!!
  /**
  * Realiza una peticion al servidor enviando el evento y el elemento web capturado.
  * @param {null}
  * @returns {null}
  **/
  console.log(dataToSend);
}

activateLocationModeOn = () => {
  /**
  * Activa las funciones para la captura de eventos.
  * @param {null}
  * @returns {null}
  **/
  searchAllElements();
  window.myScripts['ACTIVATED'] = true;
}

activateLocationModeOff = () => {
  /**
  * desactiva las funciones para la captura de eventos.
  * @param {null}
  * @returns {null}
  **/
  cleanOverlay();
  allElements = document.querySelectorAll('*');
  allElements.forEach(element => {
    element.removeEventListener("click", handleClick);
  });
  document.removeEventListener("mousemove", handleMouseMoveOnElement);
  window.myScripts['ACTIVATED'] = false;
}