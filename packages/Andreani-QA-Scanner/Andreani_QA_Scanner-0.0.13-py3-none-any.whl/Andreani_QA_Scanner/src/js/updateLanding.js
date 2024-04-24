// La funcion de este archivo y disponiblizar parte de la interfaz (servicios) para manipular el frontend desde el bankend y viceversa.

window.contextElement = null;
window.listObjects = [];
window.recorderActions = [];

function updateRecorderActionList(elementsClickedList) {
  window.recorderActions = elementsClickedList;
  addRecordedStepsToHtmlLanding();
}

function addRecordedStepsToHtmlLanding() {
  /**
   * Para cada acción dentro de la lista de pasos del recorder genera el código de una card para luego agregarlo a la landing
   * Actualiza los menús desplegables después de agregar elementos y desplaza la vista al último elemento agregado.
   * @returns {null}
   */
  const containerLoader = document.getElementById("containerActionsLoader");
  const lengthRecordActionsList = window.recorderActions.length;
  elementsCountSpan =
    '<span class="new badge btn-floating light-blue darken-4" data-badge-caption="">' +
    lengthRecordActionsList +
    "</span>";
  containerLoader.innerHTML = elementsCountSpan;
  const containerLoaderList = document.getElementById("containerActionsList");
  containerLoaderList.innerHTML = "";
  window.recorderActions.forEach(function (element, index) {
    let recorderBlock;
    if (element.event === "screenshot") {
      recorderBlock = `
            <div id="ActionBox${index}">
                <div class="row valign-wrapper margin-tb-1">
                    <div class="col s12 blue-grey lighten-5 rounded-tiny padding-tb-1 z-depth-1">
                        <div class="chip">${element.order}</div>
                        <span>Captura de pantalla</span>
                        <button class="dropdown-trigger hoverable btn btn-floating btn-small blue-grey darken-4 blue-grey-text text-lighten-4 btn-margin right" data-target="cardsDropDown_${index}">
                            <i class="material-icons Tiny">more_horiz</i>
                        </button>
                        <ul id="cardsDropDown_${index}" class="dropdown-content">
                        <li class="blue-grey lighten-4 blue-grey-hover" onclick="deleteCard(${index})">
                            <a class="blue-grey-text text-darken-4">Eliminar Paso</a>
                        </li>
                        </ul>
                        <div class="valign-wrapper">
                            <span class="left margin-l-1 material-icons">camera</span>
                            <input type="text" disabled value='${element.value}'>
                        </div>
                    </div>
                </div>
            </div>`;
    }
    if (element.event === "url log") {
      recorderBlock = `
            <div id="ActionBox${index}">
                <div class="row valign-wrapper margin-tb-1">
                    <div class="col s12 blue-grey lighten-5 rounded-tiny padding-tb-1 z-depth-1">
                        <div class="chip">${element.order}</div>
                        <span>Ingreso a la web</span>
                        <button class="dropdown-trigger hoverable btn btn-floating btn-small blue-grey darken-4 blue-grey-text text-lighten-4 btn-margin right" data-target="cardsDropDown_${index}">
                            <i class="material-icons Tiny">more_horiz</i>
                        </button>
                        <ul id="cardsDropDown_${index}" class="dropdown-content">
                        <li class="blue-grey lighten-4 blue-grey-hover" onclick="deleteCard(${index})">
                            <a class="blue-grey-text text-darken-4">Eliminar Paso</a>
                        </li>
                        </ul>
                        <div class="valign-wrapper">
                            <span class="left margin-l-1 material-icons">link</span>
                            <input type="text" disabled value='${element.value}'>
                        </div>
                    </div>
                </div>
            </div>`;
    }
        if (element.event === "open browser") {
      recorderBlock = `
            <div id="ActionBox${index}">
                <div class="row valign-wrapper margin-tb-1">
                    <div class="col s12 blue-grey lighten-5 rounded-tiny padding-tb-1 z-depth-1">
                        <div class="chip">${element.order}</div>
                        <span>Abriendo el navegador seleccionado</span>
                        <button class="dropdown-trigger hoverable btn btn-floating btn-small blue-grey darken-4 blue-grey-text text-lighten-4 btn-margin right" data-target="cardsDropDown_${index}">
                            <i class="material-icons Tiny">more_horiz</i>
                        </button>
                        <ul id="cardsDropDown_${index}" class="dropdown-content">
                        <li class="blue-grey lighten-4 blue-grey-hover" onclick="deleteCard(${index})">
                            <a class="blue-grey-text text-darken-4">Eliminar Paso</a>
                        </li>
                        </ul>
                        <div class="valign-wrapper">
                            <span class="left margin-l-1 material-icons">open_in_browser</span>
                            <input type="text" disabled value='${element.value}'>
                        </div>
                    </div>
                </div>
            </div>`;
    }


    if (element.event === "click") {
      recorderBlock = `
            <div id="ActionBox${index}">
                <div class="row valign-wrapper margin-tb-1">
                    <div class="col s12 blue-grey lighten-5 rounded-tiny padding-tb-1 z-depth-1">
                        <div class="chip">${element.order}</div>
                        <span>Realizó click en</span>
                        <button class="dropdown-trigger hoverable btn btn-floating btn-small blue-grey darken-4 blue-grey-text text-lighten-4 btn-margin right" data-target="cardsDropDown_${index}">
                            <i class="material-icons Tiny">more_horiz</i>
                        </button>
                        <ul id="cardsDropDown_${index}" class="dropdown-content">
                        <li class="blue-grey lighten-4 blue-grey-hover" onclick="deleteCard(${index})">
                            <a class="blue-grey-text text-darken-4">Eliminar Paso</a>
                        </li>
                        </ul>
                        <div class="valign-wrapper">
                            <span class="left margin-l-1 material-icons">view_in_ar</span>
                            <input type="text" disabled value='${element.target.XPATH}'/>
                        </div>
                        <span>Frame: <b>"${element.frame}"</b></span>
                    </div>
                </div>
            </div>`;
    }
    if (element.event === "input") {
      recorderBlock = `
            <div id="ActionBox${index}">
                <div class="row valign-wrapper margin-tb-1">
                    <div class="col s12 blue-grey lighten-5 rounded-tiny padding-tb-1 z-depth-1">
                        <div class="chip">${element.order}</div>
                        <span>Escribió en</span>
                        <button class="dropdown-trigger hoverable btn btn-floating btn-small blue-grey darken-4 blue-grey-text text-lighten-4 btn-margin right" data-target="cardsDropDown_${index}">
                            <i class="material-icons Tiny">more_horiz</i>
                        </button>
                        <ul id="cardsDropDown_${index}" class="dropdown-content">
                        <li class="blue-grey lighten-4 blue-grey-hover" onclick="deleteCard(${index})">
                                <a class="blue-grey-text text-darken-4">Eliminar Paso</a>
                            </li>
                        </ul>
                        <div class="valign-wrapper">
                            <span class="left margin-l-1 material-icons">view_in_ar</span>
                            <input class="right" type="text" disabled value='${element.target.XPATH}'>
                        </div>
                        <div class="valign-wrapper">
                            <span class="left margin-l-1 material-icons">create</span>
                            <input class="right" type="text" disabled value='${element.value}'>
                        </div>
                        <span>Frame: <b>"${element.frame}"</b></span>
                    </div>
                </div>
            </div>`;
    }
    if (element.event === "send_key") {
      recorderBlock = `
            <div id="ActionBox${index}">
                <div class="row valign-wrapper margin-tb-1">
                    <div class="col s12 blue-grey lighten-5 rounded-tiny padding-tb-1 z-depth-1">
                        <div class="chip">${element.order}</div>
                        <span>Presionó en</span>
                        <button class="dropdown-trigger hoverable btn btn-floating btn-small blue-grey darken-4 blue-grey-text text-lighten-4 btn-margin right" data-target="cardsDropDown_${index}">
                            <i class="material-icons Tiny">more_horiz</i>
                        </button>
                        <ul id="cardsDropDown_${index}" class="dropdown-content">
                        <li class="blue-grey lighten-4 blue-grey-hover" onclick="deleteCard(${index})">
                                <a class="blue-grey-text text-darken-4">Eliminar Paso</a>
                            </li>
                        </ul>
                        <div class="valign-wrapper">
                            <span class="left margin-l-1 material-icons">view_in_ar</span>
                            <input class="right" type="text" disabled value='${element.target.XPATH}'>
                        </div>
                        <div class="valign-wrapper">
                            <span class="left margin-l-1 material-icons">keyboard</span>
                            <input class="right" type="text" disabled value='${element.value}'>
                        </div>
                        <span>Frame: <b>"${element.frame}"</b></span>
                    </div>
                </div>
            </div>`;
    }
    recorderBlock = `<div id="ActionBox${index}" class="draggable" draggable="true">${recorderBlock}</div>`;

    containerLoaderList.insertAdjacentHTML("beforeend", recorderBlock);
  });

  // Drag and drop de las cards
  const draggableElements = document.querySelectorAll(".draggable");
  const dragStart = (e) => {
    e.dataTransfer.setData("text/plain", e.target.id);
    setTimeout(() => {
      e.target.classList.add("invisible");
    }, 0);
  };

  const dragEnd = (e) => {
    e.target.classList.remove("invisible");
  };

  const dragOver = (e) => {
    e.preventDefault();
  };

  const dragEnter = (e) => {
    e.preventDefault();
    e.target.classList.add("drag-over");
  };

  const dragLeave = (e) => {
    e.target.classList.remove("drag-over");
  };

  const drop = (e) => {
    e.preventDefault();
    const id = e.dataTransfer.getData("text/plain");
    const draggableElement = document.getElementById(id);
    const dropzone = e.target.closest(".draggable");
    const container = draggableElement.parentElement;

    if (draggableElement !== dropzone) {
      container.removeChild(draggableElement);
      const dropIndex = [...container.children].indexOf(dropzone);
      container.insertBefore(draggableElement, container.children[dropIndex]);

      // Actualizo el orden de las acciones del recorder basado su nueva posicion
      const currentIndex = parseInt(id.replace("ActionBox", ""));
      const newIndex = dropIndex;

      // Capturo el elemento que se esta moviendo
      const movedElement = window.recorderActions[currentIndex];
      // Lo remuevo del array
      window.recorderActions.splice(currentIndex, 1);
      // Lo inserto en la nueva posicion
      window.recorderActions.splice(newIndex, 0, movedElement);

      // Actualizo el orden de los elementos
      window.recorderActions.forEach((element, index) => {
        element.order = index + 1;
      });

      // Re-render de las cards
      addRecordedStepsToHtmlLanding();
    }

    e.target.classList.remove("drag-over");
  };

  draggableElements.forEach((element) => {
    element.addEventListener("dragstart", dragStart);
    element.addEventListener("dragend", dragEnd);
    element.addEventListener("dragover", dragOver);
    element.addEventListener("dragenter", dragEnter);
    element.addEventListener("dragleave", dragLeave);
    element.addEventListener("drop", drop);
  });

  update_dropdowns();
  dragAndDropReorderIndex();

  // Scroll al ultimo elemento del listado de cards
  const lastElementId = `ActionBox${window.recorderActions.length - 1}`;
  const lastElement = document.getElementById(lastElementId);
  if (lastElement) {
    lastElement.scrollIntoView({ behavior: "smooth", block: "end" });
  }
}

function addObjectRow(listObjects) {
  // Recibe una lista de objetos y crea el contenido del colapsable 'objectBox'.
  window.listObjects = listObjects;

  const objectsBox = document.querySelector("#objectsBox");
  const quality = document.getElementById("quality").value;
  var checks = [];
  if (document.getElementById("checkIframe").checked) {
    checks.push(document.getElementById("checkIframe").getAttribute("target"));
  }
  if (document.getElementById("checkDiv").checked) {
    checks.push(document.getElementById("checkDiv").getAttribute("target"));
  }
  if (document.getElementById("checkForm").checked) {
    checks.push(document.getElementById("checkForm").getAttribute("target"));
  }
  if (document.getElementById("checkInput").checked) {
    checks.push(document.getElementById("checkInput").getAttribute("target"));
  }
  if (document.getElementById("checkSelect").checked) {
    checks.push(document.getElementById("checkSelect").getAttribute("target"));
  }
  if (document.getElementById("checkOption").checked) {
    checks.push(document.getElementById("checkOption").getAttribute("target"));
  }
  if (document.getElementById("checkTextarea").checked) {
    checks.push(
      document.getElementById("checkTextarea").getAttribute("target")
    );
  }
  if (document.getElementById("checkButton").checked) {
    checks.push(document.getElementById("checkButton").getAttribute("target"));
  }
  if (document.getElementById("checkA").checked) {
    checks.push(document.getElementById("checkA").getAttribute("target"));
  }
  if (document.getElementById("checkSpan").checked) {
    checks.push(document.getElementById("checkSpan").getAttribute("target"));
  }
  if (document.getElementById("checkLi").checked) {
    checks.push(document.getElementById("checkLi").getAttribute("target"));
  }
  if (document.getElementById("checkImg").checked) {
    checks.push(document.getElementById("checkImg").getAttribute("target"));
  }
  objectsBox.innerHTML = "";
  var numberElement = 0;
  window.listObjects.forEach(function (element) {
    if (element.QUALITY >= quality && checks.includes(element.TAGNAME)) {
      var bloqueHTML = `<div class="row valign-wrapper">
                    <div class="col s12 blue-grey lighten-5 rounded-tiny padding-tb-1 z-depth-1">
                        <span>${element.NAME}</span>
                        <button class="dropdown-trigger hoverable btn btn-floating btn-small blue-grey darken-4 blue-grey-text text-lighten-4 btn-margin right" data-target="optionsObject-${element.NAME}">
                            <i class="material-icons Tiny">more_horiz</i>
                        </button>
                        <input type="text" disabled value="${element.XPATH}">
                        <span>Frame: <b>"${element.FRAME}"</b></span>
                    </div>
                    <ul id="optionsObject-${element.NAME}" class="dropdown-content">
                        <li class="blue-grey lighten-4 blue-grey-hover" onclick="copyElement(this)">
                            <a class="blue-grey-text text-darken-4">Copiar</a>
                        </li>
                        <li class="blue-grey lighten-4 blue-grey-hover" onclick="activateEditElement(this)">
                            <a class="blue-grey-text text-darken-4">Editar</a>
                        </li>
                        <li class="blue-grey lighten-4 blue-grey-hover" onclick="highlightElement(this)">
                            <a class="blue-grey-text text-darken-4">Señalar</a>
                        </li>
                    </ul>
                </div>`;

      objectsBox.insertAdjacentHTML("beforeend", bloqueHTML);
      numberElement = numberElement + 1;
    }
  });
  const containerLoader = document.getElementById("containerObjectLoader");
  bloqueHTML =
    '<span class="new badge btn-floating teal darken-2" data-badge-caption="" id="cantElements">' +
    numberElement +
    "</span>";
  containerLoader.innerHTML = bloqueHTML;
  refreshMessage("Se han encontrado " + numberElement + " elementos.");
  const cantElements = document.getElementById("cantElements");
  pulseEfects(cantElements);
  update_dropdowns();
}

function addInfractionRow(listInfractions) {
  const infractionsBox = document.querySelector("#infractionsBox");
  infractionsBox.innerHTML = "";
  var numberInfraction = 1;
  const groupedInfractions = listInfractions.reduce((list, infraction) => {
    const category = infraction.ID;
    if (!list[category]) {
      list[category] = [];
    }
    list[category].push(infraction);
    return list;
  }, {});
  for (const category in groupedInfractions) {
    const categoryInfo = groupedInfractions[category][0]["MORE_INFO"];
    const categoryLink = groupedInfractions[category][0]["INFO_URL"];
    const categoryTags = groupedInfractions[category][0]["TAGS"];
    var generarBloqueTags = function (categoryTags) {
      let bloqueTags = "";
      for (let tag of categoryTags) {
        if (tag == "wcag2a" || tag == "wcag2aa") {
          bloqueTags +=
            '<div class="chip red darken-2 white-text">' + tag + "</div>";
        } else {
          bloqueTags += '<div class="chip">' + tag + "</div>";
        }
      }
      return bloqueTags;
    };
    var bloqueHTML = `<div class="card blue-grey lighten-5 z-depth-1 rounded-small">
                <div class="card-content blue-grey lighten-5" name="${category}">
                    <div id="icon-container" style="position: relative;" class="right">
                        <button class="dropdown-trigger hoverable btn-floating btn-small blue-grey darken-4 blue-grey-text text-lighten-4 btn-margin right" data-target="optionsInfractions-${category}">
                            <i class="material-icons Tiny">more_horiz</i>
                        </button>
                    </div>
                    <span href="${categoryLink}" class="card-title blue-gray-text text-darken-4">Clave: ${category}</span>
                    <p id="cardParagraph">${categoryInfo}</p>
                    <ul id="optionsInfractions-${category}" class="dropdown-content">
                        <li class="blue-grey lighten-4 blue-grey-hover" onclick="highlightInfraction(this)">
                            <a class="blue-grey-text text-darken-4">Señalar</a>
                        </li>
                        <li class="blue-grey lighten-4 blue-grey-hover" onclick="reportIssue(this)">
                            <a class="blue-grey-text text-darken-4">Reportar</a>
                        </li>
                    </ul>
                </div>
                <div class="card-action blue-grey lighten-3 rounded-small">${generarBloqueTags(
                  categoryTags
                )}
                </div>
            </div>`;

    infractionsBox.insertAdjacentHTML("beforeend", bloqueHTML);
    numberInfraction = numberInfraction + 1;
  }

  const containerLoader = document.getElementById("containerInfractionLoader");
  bloqueHTML =
    '<span class="new badge btn-floating red darken-2" data-badge-caption="" id="cantInfractions">' +
    numberInfraction +
    "</span>";
  containerLoader.innerHTML = bloqueHTML;
  refreshMessage("Se han encontrado " + numberInfraction + "  infracciones.");
  const cantInfractions = document.getElementById("cantInfractions");
  pulseEfects(cantInfractions);
  update_dropdowns();
}

function update_dropdowns() {
  var options = {
    alignment: "right", // Cambia la alineación del dropdown
    startOnClick: true, // No cierra el dropdown al hacer clic en una opción
    constrainWidth: false,
    coverTrigger: false,
    inDuration: 300, // Cambia la duración de la animación de entrada
    outDuration: 200, // Cambia la duración de la animación de salida
  };
  var elems = document.querySelectorAll(".dropdown-trigger");
  var instances = M.Dropdown.init(elems, options);
}

function activateEditElement(buttonEdit) {
  var cancelEditElement = document.getElementById("cancelEditElement");
  var saveEditElement = document.getElementById("saveEditElement");

  if (cancelEditElement !== null) {
    var input = cancelEditElement.parentNode.querySelector("div input");
    input.disabled = true;
    input.value = window.contextElement;
    cancelEditElement.remove();
    saveEditElement.remove();
  }
  const rowObject = buttonEdit.parentNode.parentNode;
  var bloqueHTML = `<button class="btn teal darken-1" id="saveEditElement" onclick="saveElementXpath(this)">
            <i class="material-icons Tiny">check</i>
            </button>
            <button class="btn red darken-3" id="cancelEditElement" onclick="cancelElementXpath(this)">
                <i class="material-icons Tiny">close</i>
        </button>`;

  rowObject.insertAdjacentHTML("beforeend", bloqueHTML);
  const inputObject = rowObject.querySelector("div input");
  inputObject.disabled = false;
  window.contextElement = inputObject.value;
}

function saveElementXpath(buttonSave) {
  const inputObject = buttonSave.parentNode.querySelector("div input");
  const spanObject = buttonSave.parentNode.querySelector("div span");
  const buttonCancel = document.getElementById("cancelEditElement");
  inputObject.disabled = true;
  if (inputObject.value == "") {
    inputObject.value = window.contextElement;
  }
  buttonCancel.remove();
  buttonSave.remove();
  update_element(spanObject.innerHTML, inputObject.value);
}

function cancelElementXpath(buttonCancel) {
  const inputObject = buttonCancel.parentNode.querySelector("div input");
  const buttonSave = document.getElementById("saveEditElement");
  inputObject.value = window.contextElement;
  inputObject.disabled = true;
  buttonCancel.remove();
  buttonSave.remove();
}

function update_element(name, xpath) {
  pywebview.api.call_update_element(name, xpath);
}

async function startLoader(id, color = "red") {
  let containerLoader = document.getElementById(id);
  containerLoader.innerHTML = "";
  var bloqueHTML = `<div class="preloader-wrapper small active right">
            <div class="spinner-layer spinner-${color}-only">
                <div class="circle-clipper left">
                    <div class="circle"></div>
                </div>
                <div class="gap-patch">
                    <div class="circle"></div>
                </div>
                <div class="circle-clipper right">
                    <div class="circle"></div>
                </div>
            </div>
        </div>`;

  containerLoader.insertAdjacentHTML("beforeend", bloqueHTML);
}

function endLoader(id) {
  let containerLoader = document.getElementById(id);
  containerLoader.innerHTML = "";
}

async function pulseEfects(elementDOM) {
  elementDOM.classList.add("pulse");
  await wait(10000);
  elementDOM.classList.remove("pulse");
}

function wait(ms) {
  // realiza una espera.
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function highlightElement(buttonAction) {
  // LLama a la funcion call_highlight cuando se presiona un boton desde la vista.
  const valueXpath = buttonAction.parentNode.parentNode.querySelector("input");
  const nameObject = buttonAction.parentNode.parentNode.querySelector("span");
  pywebview.api.call_highlight_element(
    valueXpath.value,
    nameObject.textContent
  );
}

function copyElement(buttonAction) {
  // LLama a la funcion call_highlight cuando se presiona un boton desde la vista.
  const nameObject =
    buttonAction.parentNode.parentNode.querySelector("span").textContent;
  console.log(nameObject);
  pywebview.api.call_copy_element(nameObject);
}

function highlightInfraction(buttonHighlighInfraction) {
  const card = buttonHighlighInfraction.parentNode.parentNode.parentNode;
  pywebview.api.call_highlight_infraction(card.getAttribute("name"));
}

function reportIssue(button) {
  const card = button.parentNode.parentNode.parentNode;
  pywebview.api.call_report_infraction(card.getAttribute("name"));
}

async function refreshMessage(message) {
  // Actualiza el string del objeto 'messageLog'
  const messageContainer = document.getElementById("messageLog");
  let opacity = 1;
  while (opacity > 0) {
    messageContainer.style.opacity = opacity;
    await wait(50);
    opacity -= 0.15;
  }
  messageContainer.innerHTML = "<b>Evento</b>: " + message;
  opacity = 0;
  while (opacity < 1) {
    messageContainer.style.opacity = opacity;
    await wait(50);
    opacity += 0.15;
  }
}

function refreshObjects() {
  if (window.listObjects.length !== 0) {
    addObjectRow(window.listObjects);
  }
}

function checksAll(checkbox) {
  const formTags = document.querySelectorAll("#formTags input");
  if (checkbox.checked) {
    formTags.forEach(function (checkTag) {
      checkTag.checked = true;
    });
  } else {
    formTags.forEach(function (checkTag) {
      checkTag.checked = false;
    });
  }
  refreshObjects();
}

function deleteActionsCards() {
  const modalInstance = M.Modal.getInstance(
    document.getElementById("deleteStepsModal")
  );
  deleteAllSteps();
  modalInstance.close();
}

function showDeleteActionsConfirmation() {
  const modalInstance = M.Modal.getInstance(
    document.getElementById("deleteStepsModal")
  );
  const lengthRecordActionsList = window.recorderActions.length;

  if (lengthRecordActionsList >= 20) {
    modalInstance.open();
  } else {
    deleteActionsCards();
  }
}

function cancelDeleteActions() {
  const modalInstance = M.Modal.getInstance(
    document.getElementById("deleteStepsModal")
  );
  modalInstance.close();
}

function deleteCard(cardSelectedIndex) {
  deleteCardStep(cardSelectedIndex);
}

function dragAndDropReorderListIndexs() {
  reoderCardsIndexs(window.recorderActions);
}

document.addEventListener("DOMContentLoaded", function () {
  var modal = document.getElementById("deleteStepsModal");
  var modalInstance = M.Modal.init(modal, {});
});
