window.myFrame = '';
let controlFrames = [];
let myElements = [];
window.addEventListener('message', handleMessage);

startAutomation = () => {
  if (onIframe() === false) {
    localStorage.setItem('myElementsCache', JSON.stringify([]));
    localStorage.setItem('MyInfractionsCache', JSON.stringify([]));
    window.myFrame = 'ROOT';
  }
  if (window.myFrame === '') {
    window.parent.postMessage({ type: 'getXpathFrame' }, '*');
  }
}

function onIframe() {
  try {
    if (window.self === window.top) {
      console.log("Estoy en el frame principal... ", window.location.href);
      return false;
    } else {
      console.log("Estoy en un iframe... ", window.location.href);
      return true;
    }
  } catch (e) {
    console.log("Estoy en un iframe... ", window.location.href);
    return true; // En caso de que haya restricciones de seguridad, asumimos que estamos en un iframe
  }
}
const getXpathFrame = () => {
  let iframes = document.getElementsByTagName("iframe");
  for (var j = 0; j < iframes.length; j++) {
    var xpathFrame = buildXpaths("iframe", iframes[j]);
    iframes[j].contentWindow.postMessage({ type: "refreshXpathFrame", data: xpathFrame.XPATH }, '*');
  }
}
const scann =() => {
  /**
  * Realiza el escaneo de todos los objetos web que cumplan con las condiciones requeridas para la captura de los elementos automatizables.
  * @param {null}
  * @returns {null}
  **/
  if (onIframe() === false) {
    localStorage.setItem('myElementsCache', JSON.stringify([]));
    window.myFrame = 'ROOT';
  }
  if (window.myFrame !== '') {
    myElements = [];
    const allElements = ["iframe", "div", "form", "table", "input", "select", "option", "textarea", "button", "a", "span", "img", "svg", "li"]; // Carga todos los tag de los elementos que se desean capturar.

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
      else if (tagnam == "select" || tagnam == "textarea" || tagnam == "button" || tagnam == "a" || tagnam == "span" || tagnam == "img" || tagnam == "svg" || tagnam == "li") {
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
      else if (tagnam === "iframe") {
        for (k = 0; k < len; k++) {
          buildXpaths(tagnam, elements[k]); // realiza la construccion del xpath.
        }
      }
    }
    if (window.myFrame === 'ROOT') {
      localStorage.setItem('myElementsCache', JSON.stringify(myElements));
      let iframes = document.getElementsByTagName('iframe');
      for (let i = 0; i < iframes.length; i++) {
        iframes[i].contentWindow.postMessage({ type: 'refreshElements' }, '*');
      }
    } else {
      window.parent.postMessage({ type: 'elementsOniFrame', data: myElements }, '*');
    }
  } else {
    window.parent.postMessage({ type: 'getXpathFrame' }, '*');
  }
}

buildXpaths = (tagnam, element) => {
  /**
  * Llama a las funciones encargadas de obtener los xpath de los elementos web.
  * @param {string} tagnam - es el tagname del elemento que se recibe.
  * @param {object} element - elemento web del cual se obtendra el xpath.
  * @returns {null}
  **/
  if (element.hasAttribute("id")) {
    return getTargetById(tagnam, element); // Armara el xpath si el atributo tiene id.

  } else if (element.hasAttribute("name")) {
    return getTargetByName(tagnam, element); // Armara el xpath si el atributo tiene name.

  } else if (element.hasAttribute("formcontrolname")) {
    return getTargetByFormControlName(tagnam, element); // Armara el xpath si el atributo tiene formcontrolname.

  } else if (element.hasAttribute("placeholder")) {
    return getTargetPlaceholder(tagnam, element); // Armara el xpath si el atributo tiene placeholder.

  } else if (element.hasAttribute("value")) {
    return getTargetByValue(tagnam, element); // Armara el xpath si el atributo tiene value.

  } else if (element.hasAttribute("role")) {
    return getTargetByRole(tagnam, element); // Armara el xpath si el atributo tiene role.

  } else if (element.hasAttribute("alt")) {
    return getTargetByAlt(tagnam, element); // Armara el xpath si el atributo tiene alt.

  } else if (element.hasAttribute("class") && tagnam != "button" && tagnam != "a" && tagnam != "span") {
    return getTargetByclass(tagnam, element); // Armara el xpath si el atributo tiene class mientras no sea button, a o span.
  }
  else if (tagnam == "button" || tagnam == "a" || tagnam == "input" || tagnam == "span" || tagnam == "li" || tagnam == "option") {
    return getTargetByText(tagnam, element); // Armara el xpath si el atributo tiene text mientras el tag sea button, a, input, span, li u option
  } else {
    return getTargetByGeneric(tagnam, element);
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
    'FRAME': window.myFrame,
    'QUALITY': quality
  }
  return validateElement(objectTarget);
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
    'FRAME': window.myFrame,
    'QUALITY': quality
  };
  return validateElement(objectTarget);
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
    'FRAME': window.myFrame,
    'QUALITY': quality
  };
  return validateElement(objectTarget);
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
    'FRAME': window.myFrame,
    'QUALITY': quality
  };
  return validateElement(objectTarget);
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
    'FRAME': window.myFrame,
    'QUALITY': quality
  };
  return validateElement(objectTarget);
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
    'FRAME': window.myFrame,
    'QUALITY': quality
  };
  return validateElement(objectTarget);
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
    'FRAME': window.myFrame,
    'QUALITY': quality
  };
  return validateElement(objectTarget);
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
    'FRAME': window.myFrame,
    'QUALITY': quality
  };
  return validateElement(objectTarget);
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
    'FRAME': window.myFrame,
    'QUALITY': quality
  };
  return validateElement(objectTarget);
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
    'FRAME': window.myFrame,
    'QUALITY': 0
  };
  return validateElement(objectTarget);
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
    if (result.snapshotLength !== 1) {
      const newXpath = getXpathByFatherSon(xpath, element);
      const newResult = document.evaluate(newXpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
      if (newResult.snapshotLength === 1) {
        xpath = newXpath;
        quality = 1;
      } else {
        xpath = generateXPath(element);
        quality = 0;
      }
    }
  } catch (error) {
    xpath = generateXPath(element);
    quality = 0;
  } finally{
    return [xpath, quality]
  }
};

const generateXPath = (domElement, absolute = false) => {
  /**
  * Generar xpath relativo o absolutos cuando el resto de metodos no pueden armar un xpath mas robusto.
  * @param {object} domElement - Elemento web.
  * @returns {string} xpath - xpath absoluto o relativo.
  **/
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
  const elementTarget = document.evaluate(element['XPATH'], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

  try {
    if (element['TAGNAME'] === "<iframe>") {
      elementTarget.contentWindow.postMessage({ type: "refreshXpathFrame", data: element['XPATH']}, '*');
      return element
    }
    if (elementTarget.getClientRects()[0] !== undefined || elementTarget.getClientRects()[0] !== null) {
      if (elementTarget.getClientRects()[0].left !== undefined || elementTarget.getClientRects()[0].top !== undefined || elementTarget.getClientRects()[0].width !== undefined || elementTarget.getClientRects()[0].width !== undefined) {
        myElements.push(element);
        myElements.unshift(myElements.pop());
        return element;
      }
    }
  } catch (error) {
    //
  }
};

// Manejar mensajes del frame principal
function handleMessage(event) {
  const jsonRecoveredMyElements = JSON.parse(localStorage.getItem('myElementsCache'));
  const newElementsList = [];
  if (event.data.type === 'refreshElements') {
    scann();
  }
  if (event.data && event.data.type === 'refreshXpathFrame') {
    window.myFrame = event.data.data;
  }
  if (event.data && event.data.type === 'getXpathFrame') {
    getXpathFrame();
  }

  if(event.data && event.data.type === "refreshInfractions"){
    runScannAxe();
  }

  if (event.data && event.data.type === 'infractionsOnFrame') {
    let jsonMyInfractions = JSON.parse(localStorage.getItem('MyInfractionsCache'));
    console.log(jsonMyInfractions);
    jsonMyInfractions.push(...event.data.data);
    localStorage.setItem('MyInfractionsCache', JSON.stringify(jsonMyInfractions));
  }


  if (event.data && event.data.type === 'elementsOniFrame') {
    const elementList = event.data.data;
    if (jsonRecoveredMyElements !== null) {
      for (j = 0; j < elementList.length; j++) {
        let searchObject = jsonRecoveredMyElements.find(element => JSON.stringify(element) === JSON.stringify(elementList[j]));
        if (!searchObject) {
          jsonRecoveredMyElements.push(elementList[j]);
        }
      }
    }
  }
  localStorage.setItem('myElementsCache', JSON.stringify(jsonRecoveredMyElements));
}

startAutomation();