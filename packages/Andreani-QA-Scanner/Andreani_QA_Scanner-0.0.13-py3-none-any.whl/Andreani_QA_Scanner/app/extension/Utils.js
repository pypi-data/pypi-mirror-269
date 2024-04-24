buildResponseBody = (callName, myElement, value = null) => {
    /**
    * Dependiendo del parametro recibido se genera el payload a enviar al backend
    * @param {string} callName 
    * @returns {Object|null} 
    **/
    return {
        // si se llama tanto del recorder con un evento click o input, o si se esta utilizando en modo inspector
        event: callName,
        target: myElement,
        value: value,
        frame: myElement["FRAME"]
    };
};

call_listener_log_events = (payload) => {
    /**
    * Realiza una peticion al backend enviando el payload del evento.
    * @param {string} payload  
    * @returns {null}
    **/ 
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    const requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: JSON.stringify(payload),
        redirect: 'follow'
    };
    let eventsUrl = "http://127.0.0.1:30505/api/events";
    fetch(eventsUrl, requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));
}


// Escucha un evento para realizar el escaneo.
document.addEventListener("runScann", function () {
    scann();
  });

// Escucha un evento para realizar el escaneo.
document.addEventListener("runAxe", function () {
    localStorage.setItem('MyInfractionsCache', JSON.stringify([]));
    startAxe();
  });

// Escucha un evento para realizar el escaneo.
document.addEventListener("runMonkeyTest", function () {
    monkeyTest();
  });

highlight = (expression, typeElement, scroll) => {
  /**
  * Convierte la expresion en un elemento web y lo señala en pantalla.
  * @param {string} expression - xpath o queryselector que representa un objeto web.
  * @param {string} typeElement - indica si es un xpath o un queryselector.
  * @param {bool} scroll - Indica si debe scrollear la pantalla antes de señalar el elemento.
  * @returns {bool} Retorna si pudo o no señalar el elemento.
  **/
  try {
    let elementTarget, colorBox, time;
    if (typeElement === 'XPATH') {
      elementTarget = document.evaluate(expression, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
      colorBox = 'green';
      time= 3000;
    }else if (typeElement === 'OBJECT') {
        elementTarget = document.evaluate(expression, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        colorBox = 'blue';
        time= 1000;
    } else if (typeElement === 'CSS') {
      elementTarget = document.querySelector(expression);
      colorBox = 'red';
      time= 3000;
    }

    if (elementTarget) {
      if (scroll === true) {
        elementTarget.scrollIntoView({
          behavior: 'auto',
          block: 'end',
        });
      }
      const box = document.createElement('div');
      box.classList.add('box');
      document.body.appendChild(box);
      const elementTargetRect = elementTarget.getClientRects()[0];
      box.style.left = `${elementTargetRect.left}px`;
      box.style.top = `${elementTargetRect.top}px`;
      box.style.width = `${elementTargetRect.width}px`;
      box.style.height = `${elementTargetRect.height}px`;
      const style = document.createElement('style');
      style.textContent = `
        .box {
          position: absolute;
          z-index: 9999 !important;
          background-color: None;
          border: 3px solid ${colorBox};
          animation: titilar 1s infinite;
        }

        @keyframes titilar {
          0% {
            opacity: 1;
          }
          50% {
            opacity: 0.5;
          }
          100% {
            opacity: 1;
          }
        }
      `;
      document.head.appendChild(style);
      setTimeout(() => {
        document.body.removeChild(box);
        document.head.removeChild(style);
      }, time);
    } else {
      console.log('No es posible señalar ' + expression);
      return false;
    }
  } catch (error) {
    console.error(error);
    console.log('Error en la expresion xpath ' + expression);
    return false;
  }
  return true;
};
