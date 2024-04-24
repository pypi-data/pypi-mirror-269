// Funciones que permiten el escaneo de las web.
window.myScanner = true;
window.myIframeObjects = []
window.my_elements = []
window.urlDomain // variable para identificar url (sin subdominio ni query params)

try {
  // Intenta remover el listener
  window.removeEventListener('message', handleMessage);
} catch (error) {
  // Maneja cualquier excepción que pueda ocurrir
}

scann = () => {
  /**
  * Realiza el escaneo de todos los objetos web que cumplan con las condiciones requeridas para la captura de los elementos automatizables.
  * @param {null}
  * @returns {null}
  **/
  const allElements = ["iframe", "div", "form", "table", "input", "select", "option", "textarea", "button", "a", "span", "img", "li"]; // Carga todos los tag de los elementos que se desean capturar.

  // recorre cada uno de los elementos de la lista que resultan de interes para la automatizacion.
  for (j = 0; j < allElements.length; j++) {
    let tagnam = allElements[j];
    let elements = document.getElementsByTagName(tagnam); // genera una lista con los elementos encontrados a partir del tipo de tag.
    let len = elements.length; // Obtiene el numero de elementos.
    // Flujo de trabajo para el armado de xpath de los inputs encontrados en el DOM.
    if (tagnam == "input") {
      for (i = 0; i < len; i++) {
        if (elements[i].getAttribute("type") != "hidden") { // El input esta visible?
          if (elements[i].getAttribute("style") == null) { // Si el elemento input no tiene estilos
            buildXpaths(tagnam, elements[i]); // realiza la construccion del xpath
          } else if ((elements[i].getAttribute("style") != null) && (!elements[i].getAttribute("style").includes("display"))) { // Si el elemento tiene estilos y Si el elemento tiene asociada un string.
            buildXpaths(tagnam, elements[i]); // realiza la construccion del xpath

          }
        }
      }
    }
    // Flujo de trabajo para el armado de xpath para un conjunto de elementos encontrados en el DOM.
    else if (tagnam == "select" || tagnam == "textarea" || tagnam == "button" || tagnam == "a" || tagnam == "span" || tagnam == "img" || tagnam == "li") {
      for (k = 0; k < len; k++) {
        if (elements[k].getAttribute("style") == null) { // Si el elemento input no tiene estilos
          buildXpaths(tagnam, elements[k]); // realiza la construccion del xpath.
        } else if (elements[k].getAttribute("style") != null) { // Si el elemento tiene estilos.
          if (!elements[k].getAttribute("style").includes("display")) { // Si el elemento tiene asociada un string.
            buildXpaths(tagnam, elements[k]); // realiza la construccion del xpath.
          }
        }
      }
    }
    // Flujo de trabajo para el armado de xpath de elementos de tipo div elementos encontrados en el DOM.
    else if (tagnam == "div") {
      for (k = 0; k < len; k++) {
        let textOnDiv = '';
        for (const childNode of elements[k].childNodes) {
          if (childNode.nodeType === Node.TEXT_NODE) {
            // Verificar si es un nodo de texto
            textOnDiv += childNode.textContent;
          }
        }
        if (elements[k].getAttribute("style") == null && elements[k].getAttribute("draggable") == "true") { // Si el elemento div no tiene estilos pero que tenga el atributos draggable en "true".
          buildXpaths(tagnam, elements[k]); // realiza la construccion del xpath.
        } else if (elements[k].getAttribute("role") == "button") { // Si el elemento div tiene estilos pero que tenga el atributos role "button".
          buildXpaths(tagnam, elements[k]); // realiza la construccion del xpath.
        } else if (textOnDiv.trim() !== '') {
          buildXpaths(tagnam, elements[k]);
        }
      }
    }
    // Flujo de trabajo para el armado de xpath de elementos de tipo iframes encontrados en el DOM.
    else if (tagnam == "iframe") {
      for (k = 0; k < len; k++) {
        buildXpaths(tagnam, elements[k]); // realiza la construccion del xpath.
      }
    }
  }
  loadElements(my_elements); // arreglo con los objetos encontrados
}

buildXpaths = (tagnam, element) => {
  /**
  * Llama a las funciones encargadas de obtener los xpath de los elementos web.
  * @param {string} tagnam - es el tagname del elemento que se recibe.
  * @param {object} element - elemento web del cual se obtendra el xpath.
  * @returns {null}
  **/
  if (element.hasAttribute("id")) {
    getTargetById(tagnam, element); // Armara el xpath si el atributo tiene id.

  } else if (element.hasAttribute("name")) {
    getTargetByName(tagnam, element); // Armara el xpath si el atributo tiene name.

  } else if (element.hasAttribute("formcontrolname")) {
    getTargetByFormControlName(tagnam, element); // Armara el xpath si el atributo tiene formcontrolname.

  } else if (element.hasAttribute("placeholder")) {
    getTargetPlaceholder(tagnam, element); // Armara el xpath si el atributo tiene placeholder.

  } else if (element.hasAttribute("value")) {
    getTargetByValue(tagnam, element); // Armara el xpath si el atributo tiene value.

  } else if (element.hasAttribute("role")) {
    getTargetByRole(tagnam, element); // Armara el xpath si el atributo tiene role.

  } else if (element.hasAttribute("alt")) {
    getTargetByAlt(tagnam, element); // Armara el xpath si el atributo tiene alt.

  } else if (element.hasAttribute("class") && tagnam != "button" && tagnam != "a" && tagnam != "span") {
    getTargetByclass(tagnam, element); // Armara el xpath si el atributo tiene class mientras no sea button, a o span.
  }
  else if (tagnam == "button" || tagnam == "a" || tagnam == "input" || tagnam == "span" || tagnam == "li" || tagnam == "option") {
    getTargetByText(tagnam, element); // Armara el xpath si el atributo tiene text mientras el tag sea button, a, input, span, li u option
  } else {
    getTargetByGeneric(tagnam, element);
  }
}

const getTargetByAlt = (tagElement, element) => {
  /**
  * Arma un xpath utilizando el atributo Alt y lo agrega en un json.
  * @param {string} tagElement - es el tagname del elemento que se recibe.
  * @param {object} element - elemento web del cual se obtendra el xpath.
  * @returns {null}
  **/

  const alt = element.getAttribute("alt");
  const target = "//" + tagElement + "[@alt=\"" + alt + "\"]";
  const [xpath, quality] = evaluate_xpath(target, element, 2);
  const objectTarget = {
    'TAGNAME': '<' + tagElement + '>',
    'XPATH': xpath,
    'FRAME': myFrame,
    'QUALITY': quality
  };
  //console.log("getTargetByAlt: " + objectTarget['XPATH'] + " : " + objectTarget['QUALITY']);
  validateElement(objectTarget);
}

const getTargetById = (tagElement, element) => {
  /**
  * Arma un xpath utilizando el atributo id y lo agrega en un json.
  * @param {string} tagElement - es el tagname del elemento que se recibe.
  * @param {object} element - elemento web del cual se obtendra el xpath.
  * @returns {null}
  **/

  const id = element.getAttribute("id");
  const target = "//" + tagElement + "[@id=\"" + id + "\"]";
  const [xpath, quality] = evaluate_xpath(target, element, 3);
  const objectTarget = {
    'TAGNAME': '<' + tagElement + '>',
    'XPATH': xpath,
    'FRAME': myFrame,
    'QUALITY': quality
  };
  //console.log("getTargetById: " + objectTarget['XPATH'] + " : " + objectTarget['QUALITY']);
  validateElement(objectTarget);
}

const getTargetByName = (tagElement, element) => {
  /**
  * Arma un xpath utilizando el atributo id y lo agrega en un json.
  * @param {string} tagElement - es el tagname del elemento que se recibe.
  * @param {object} element - elemento web del cual se obtendra el xpath.
  * @returns {null}
  **/
  const name = element.getAttribute("name");
  const target = "//" + tagElement + "[@name=\"" + name + "\"]";
  const [xpath, quality] = evaluate_xpath(target, element, 2);
  const objectTarget = {
    'TAGNAME': '<' + tagElement + '>',
    'XPATH': xpath,
    'FRAME': myFrame,
    'QUALITY': quality
  };
  //console.log("getTargetByName: " + objectTarget['XPATH'] + " : " + objectTarget['QUALITY']);
  validateElement(objectTarget);
}

const getTargetByFormControlName = (tagElement, element) => {
  /**
  * Arma un xpath utilizando el atributo formcontrolname y lo agrega en un json.
  * @param {string} tagElement - es el tagname del elemento que se recibe.
  * @param {object} element - elemento web del cual se obtendra el xpath.
  * @returns {null}
  **/
  const from = element.getAttribute("formcontrolname");
  const target = "//" + tagElement + "[@formcontrolname=\"" + from + "\"]";
  const [xpath, quality] = evaluate_xpath(target, element, 2);
  const objectTarget = {
    'TAGNAME': '<' + tagElement + '>',
    'XPATH': xpath,
    'FRAME': myFrame,
    'QUALITY': quality
  };
  //console.log("getTargetByFormControlName: " + objectTarget['XPATH'] + " : " + objectTarget['QUALITY']);
  validateElement(objectTarget);
}

const getTargetPlaceholder = (tagElement, element) => {
  /**
  * Arma un xpath utilizando el atributo placeholder y lo agrega en un json.
  * @param {string} tagElement - es el tagname del elemento que se recibe.
  * @param {object} element - elemento web del cual se obtendra el xpath.
  * @returns {null}
  **/
  const ph = element.getAttribute("placeholder");
  const target = "//" + tagElement + "[@placeholder=\"" + ph + "\"]";
  const [xpath, quality] = evaluate_xpath(target, element, 2);
  const objectTarget = {
    'TAGNAME': '<' + tagElement + '>',
    'XPATH': xpath,
    'FRAME': myFrame,
    'QUALITY': quality
  };
  //console.log("getTargetPlaceholder: " + objectTarget['XPATH'] + " : " + objectTarget['QUALITY']);
  validateElement(objectTarget);
}

const getTargetByValue = (tagElement, element) => {
  /**
  * Arma un xpath utilizando el atributo value y lo agrega en un json.
  * @param {string} tagElement - es el tagname del elemento que se recibe.
  * @param {object} element - elemento web del cual se obtendra el xpath.
  * @returns {null}
  **/
  const value = element.getAttribute("value");
  const target = "//" + tagElement + "[@value=\"" + value + "\"]";
  const [xpath, quality] = evaluate_xpath(target, element, 2);
  const objectTarget = {
    'TAGNAME': '<' + tagElement + '>',
    'XPATH': xpath,
    'FRAME': myFrame,
    'QUALITY': quality
  };
  //console.log("getTargetByValue: " + objectTarget['XPATH'] + " : " + objectTarget['QUALITY']);
  validateElement(objectTarget);
}

const getTargetByRole = (tagElement, element) => {
  /**
  * Arma un xpath utilizando el atributo role y lo agrega en un json.
  * @param {string} tagElement - es el tagname del elemento que se recibe.
  * @param {object} element - elemento web del cual se obtendra el xpath.
  * @returns {null}
  **/
  const rol = element.getAttribute("role");
  const target = "//" + tagElement + "[@role=\"" + rol + "\"]";
  const [xpath, quality] = evaluate_xpath(target, element, 2);
  const objectTarget = {
    'TAGNAME': '<' + tagElement + '>',
    'XPATH': xpath,
    'FRAME': myFrame,
    'QUALITY': quality
  };
  //console.log("getTargetByRole: " + objectTarget['XPATH'] + " : " + objectTarget['QUALITY']);
  validateElement(objectTarget);
}

const getTargetByclass = (tagElement, element) => {
  /**
  * Arma un xpath utilizando el atributo class y lo agrega en un json.
  * @param {string} tagElement - es el tagname del elemento que se recibe.
  * @param {object} element - elemento web del cual se obtendra el xpath.
  * @returns {null}
  **/
  const cls = element.getAttribute("class");
  const target = "//" + tagElement + "[@class=\"" + cls + "\"]";
  const [xpath, quality] = evaluate_xpath(target, element, 2);
  const objectTarget = {
    'TAGNAME': '<' + tagElement + '>',
    'XPATH': xpath,
    'FRAME': myFrame,
    'QUALITY': quality
  };
  //console.log("getTargetByclass: " + objectTarget['XPATH'] + " : " + objectTarget['QUALITY']);
  validateElement(objectTarget);
}

const getTargetByText = (tagElement, element) => {
  /**
  * Arma un xpath utilizando el texto contenido y lo agrega en un json.
  * @param {string} tagElement - es el tagname del elemento que se recibe.
  * @param {object} element - elemento web del cual se obtendra el xpath.
  * @returns {null}
  **/
  const text = element.innerText;
  let target, quality, xpath;

  if (text !== "") {
    const listText = text.split("\n");

    if (text.length > 1) {
      target = `//${tagElement}[contains(text(),"${listText[0]}")]`;
    } else {
      target = `//${tagElement}[text()="${text}"]`;
    }

    [xpath, quality] = evaluate_xpath(target, element, 2);
  } else {
    [xpath, quality] = [generateXPath(element), 0];
  }

  const objectTarget = {
    'TAGNAME': '<' + tagElement + '>',
    'XPATH': xpath,
    'FRAME': myFrame,
    'QUALITY': quality
  };

  //console.log("getTargetByclass: " + objectTarget['XPATH'] + " : " + objectTarget['QUALITY']);
  validateElement(objectTarget);
}

const getTargetByGeneric = (tagElement, element) => {
  /**
  * Arma el full xpath del elemento y lo agrega en un json.
  * @param {string} tagElement - es el tagname del elemento que se recibe.
  * @param {object} element - elemento web del cual se obtendra el xpath.
  * @returns {null}
  **/
  const target = generateXPath(element);
  const objectTarget = {
    'TAGNAME': '<' + tagElement + '>',
    'XPATH': target,
    'FRAME': myFrame,
    'QUALITY': 0
  };
  //console.log("getTargetByclass: " + objectTarget['XPATH'] + " : " + objectTarget['QUALITY']);
  validateElement(objectTarget);
}

const getXpathByFatherSon = (xpath, element) => {
  /**
  * Arma un xpath utilizando el elemento padre y sus atributos con los del elemento objetivo.
  * @param {string} xpath - xpath del elemento web al que se le adjuntara el xpath de su div padre.
  * @param {object} element - elemento web del cual se obtendra el xpath.
  * @returns {null}
  **/
  const father = element.closest("div");
  if (father != null) {
    if (father.hasAttribute("class")) {
      return "//div[@class=\"" + father.getAttribute('class') + "\"]" + xpath
    }
    else {
      return "//div" + xpath
    }
  }
  else {
    return xpath
  }
}

const evaluate_xpath = (xpath, element, quality) => {
  /**
  * Evalua si el xpath representa un elemento univoco en la pagina.
  * @param {object} element - Elemento web.
  * @param {int} quality - Entero que representa la calidad del xpath de un elemento.
  * @returns {list} [xpath, quality] - xpath y su calidad final.
  **/
  try {
    const result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

    if (result.snapshotLength === 1) {
      return [xpath, quality];
    } else {
      const newXpath = getXpathByFatherSon(xpath, element);
      const newResult = document.evaluate(newXpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

      if (newResult.snapshotLength === 1) {
        return [newXpath, 1];
      } else {
        return [generateXPath(element), 0];
      }
    }
  } catch (error) {
    return [generateXPath(element), 0];
  }
};

const generateXPath = (domElement, absolute = false) => {
  /**
  * Generar xpath relativo o absolutos cuando el resto de metodos no pueden armar un xpath mas robusto.
  * @param {object} domElement - Elemento web.
  * @returns {string} xpath - xpath absoluto o relativo.
  **/
  if (!absolute && domElement.id.length) {
    return "//*[@id=\"" + domElement.id + "\"]";
  }
  if (!absolute && document.getElementsByTagName(domElement.tagName).length === 1) {
    return "//" + domElement.tagName.toLowerCase();
  }
  if (absolute && domElement.tagName.toLowerCase() === 'html') {
    return '/html'
  }
  const nodesInSameLevel = Array.from(domElement.parentNode.childNodes);
  const nodesInSameLevelWithSameTagName = nodesInSameLevel.filter(element => element.tagName === domElement.tagName);
  const domElementLevelPosition = nodesInSameLevelWithSameTagName.indexOf(domElement);
  return `${generateXPath(domElement.parentNode, true)}/${domElement.tagName.toLowerCase()}${`[${domElementLevelPosition + 1}]`}`;
}

const validateElement = (element) => {
  /**
  * Valida si el elemento esta renderizado en la pagina y lo agrega a la lista de elementos en memoria.
  * @param {object} domElement - Elemento web.
  * @returns {null}
  **/

  if (element['TAGNAME'] !== "<iframe>") {
    const elementTarget = document.evaluate(element['XPATH'], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    if (elementTarget.getClientRects()[0] !== undefined) {
      window.my_elements.push(element);
      window.my_elements.unshift(window.my_elements.pop());
    }
  } else {
    let encontrado = my_elements.find(my_element => my_element.XPATH === element['XPATH']) !== undefined;
    if (!encontrado) {
      window.my_elements.push(element);
      window.my_elements.unshift(window.my_elements.pop());
    }
    let findedFrame = myIframeObjects.find(IframeObjects => IframeObjects.XPATH === element['XPATH']) !== undefined;
    if (!findedFrame) {
      window.myIframeObjects.push(element);
    }
  }
}

getIframes = () => {
  let iframes = document.getElementsByTagName('iframe');
  for (j = 0; j < iframes.length; j++) {
    buildXpaths('iframe', iframes[j]);
  }
  return myIframeObjects
}

call_url_log = () => {
  call_listener_log_events("urlLog");
};

highlight = (expression, typeElement, scroll) => {
  /**
  * Convierte la expresion en un elemento web y lo señala en pantalla.
  * @param {string} expression - xpath o queryselector que representa un objeto web.
  * @param {string} typeElement - indica si es un xpath o un queryselector.
  * @param {bool} scroll - Indica si debe scrollear la pantalla antes de señalar el elemento.
  * @returns {bool} Retorna si pudo o no señalar el elemento.
  **/
  try {
    let elementTarget, colorBox;
    if (typeElement === 'XPATH') {
      elementTarget = document.evaluate(expression, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
      colorBox = 'green';
    } else if (typeElement === 'CSS') {
      elementTarget = document.querySelector(expression);
      colorBox = 'red';
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
      }, 3000);
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

const loadElements = (elements) => {
  const jsonRecoveredMyElements = JSON.parse(localStorage.getItem('MyElementsCache'));
  if (myFrame === 'MAIN') {
    const jsonMyElements = JSON.stringify(elements);
    localStorage.setItem('MyElementsCache', jsonMyElements);
  } else {
    window.parent.postMessage({ type: 'elementsOniFrame', data: elements }, '*');
  }
}

// Función de escucha
function handleMessage(event) {
  if (event.data && event.data.type === 'elementsOniFrame') {
    const elementList = event.data.data;
    const jsonRecoveredMyElements = JSON.parse(localStorage.getItem('MyElementsCache'));
    for (let i = 0; i < elementList.length; i++) {
      let encontrado = jsonRecoveredMyElements.find(element => element.XPATH === elementList[i]['XPATH']) !== undefined;
      if (!encontrado) {
        jsonRecoveredMyElements.push(elementList[i]);
      }
    }
    localStorage.setItem('MyElementsCache', JSON.stringify(jsonRecoveredMyElements));
  }
  if (event.data && event.data.type === 'infractionsOnFrame') {
    const infractionList = event.data.data;
    const jsonRecoveredMyInfractions = JSON.parse(localStorage.getItem('MyInfractionsCache'));
    for (let i = 0; i < infractionList.length; i++) {
        jsonRecoveredMyInfractions.push(infractionList[i]);
      }
    }
  }

window.addEventListener('message', handleMessage);

scann();