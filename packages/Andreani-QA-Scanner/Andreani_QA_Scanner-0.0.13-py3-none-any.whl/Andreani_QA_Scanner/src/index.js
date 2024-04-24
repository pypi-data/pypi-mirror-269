// La funcion de este archivo y disponiblizar parte de la interfaz (servicios) para manipular el frontend desde el bankend y viceversa.
function openBrowser() {
    // LLama a la funcion call_open_browser desde la vista.
    const myBrowser = document.getElementById("selectBrowser").value;
    pywebview.api.call_open_browser(myBrowser);
}

function scan() {
    // LLama a la funcion call_scan desde la vista.
    pywebview.api.call_scan();
}

function monkeyTest() {
    // LLama a la funcion call_scan desde la vista.
    pywebview.api.call_execute_monkey_test();
 }


function saveFile() {
    // LLama a la funcion call_save_to_file desde la vista.
    const quality = document.getElementById("quality").value;
    const objectsElements = window.listObjects.filter(item => item.QUALITY >= quality);
    pywebview.api.call_save_to_file(objectsElements);
}

function highLight() {
    // LLama a la funcion call_highlight desde la vista.
    const quality = document.getElementById("quality").value;
    var checks = []
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
        checks.push(document.getElementById("checkTextarea").getAttribute("target"));
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
    const objectsElements = window.listObjects.filter(item => item.QUALITY >= quality && checks.includes(item.TAGNAME));
    pywebview.api.call_highlight(objectsElements);
}

//inicio de prueba para agregar el sistema de configs para Jira
function openJiraConfigs() {
    // LLama a la funcion open_jira_config_window desde la vista.
    // los comandos que llegan a este archivo vienen desde el Landing.html
    pywebview.api.call_open_jira_config_window();
}

function inspectionElements() {
    pywebview.api.call_inspection_elements();

}


function enableConfigButton() {
    //activación del botón config
    userConfig.setAttribute('data-flag', 'true');
    //restauración del ícono configs
    var iconElement = document.getElementById('landingIcon');
    iconElement.innerText = 'settings';
}

// function monkeyTest() {
// LLama a la funcion execute_monkey_test desde la vista.
// pywebview.api.execute_monkey_test();
// }

// Funcion para que los distintos colapsables se cierren cuando uno de ellos se expande.
document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.collapsible.box');
    var instances = M.Collapsible.init(elems, {
        onOpenStart: function (el) {
            var collapsibles = document.querySelectorAll('.collapsible.box');
            for (var i = 0; i < collapsibles.length; i++) {
                if (collapsibles[i] !== el) {
                    var instance = M.Collapsible.getInstance(collapsibles[i]);
                    instance.close();
                }
            }
        }
    });
});

// Funcion para que los distintos colapsables se cierren cuando uno de ellos se expande.
document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.collapsible.filter');
    var instances = M.Collapsible.init(elems, {
        onOpenStart: function (el) {
            var collapsibles = document.querySelectorAll('.collapsible.filter');
            for (var i = 0; i < collapsibles.length; i++) {
                if (collapsibles[i] !== el) {
                    var instance = M.Collapsible.getInstance(collapsibles[i]);
                    instance.close();
                }
            }
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var options = {
        alignment: 'right', // Cambia la alineación del dropdown
        startOnClick: true, // No cierra el dropdown al hacer clic en una opción
        constrainWidth: false,
        coverTrigger: false,
        inDuration: 300, // Cambia la duración de la animación de entrada
        outDuration: 200, // Cambia la duración de la animación de salida
    };

    var elems = document.querySelectorAll('.dropdown-trigger');
    var instances = M.Dropdown.init(elems, options);
});

document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.tooltipped');
    var instances = M.Tooltip.init(elems);
});

document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems, {});
    changeColor();
});

function changeColor() {
    var dropdown_elem = document.querySelectorAll(".dropdown-content li")
    var classStyle = ["blue-grey", "lighten-4", "blue-grey-hover"];
    dropdown_elem.forEach(function (element) {
        element.classList.add(...classStyle);
    });

    var options_elem = document.querySelectorAll(".dropdown-content li>a, .dropdown-content li>span");
    var classStyle = ["blue-grey-text", "text-darken-4"];
    options_elem.forEach(function (element, index) {
        element.classList.add(...classStyle);
    });
    var options = {
        alignment: 'right', // Cambia la alineación del dropdown
        startOnClick: true, // No cierra el dropdown al hacer clic en una opción
        constrainWidth: true,
        coverTrigger: false,
        inDuration: 300, // Cambia la duración de la animación de entrada
        outDuration: 200, // Cambia la duración de la animación de salida
    };
    var elems = document.querySelectorAll('.dropdown-trigger');
    var instances = M.Dropdown.init(elems, options);
}

function getLandingStatus() {
    var landingFocus = document.getElementById('landingBlock');
    var focusFlag = landingFocus.getAttribute('data-focus');
    var iconElement = document.getElementById('focusIcon');
    var dataTooltip = landingFocus.parentNode
    if (focusFlag == 'false') {
        //si es False pasa a True
        landingFocus.setAttribute('data-focus', 'true');
        iconElement.innerText = 'flip_to_back';
        dataTooltip.setAttribute('data-tooltip', 'Enviar al fondo');
        pywebview.api.focus_landing_on();
    }
    else {
        //si es True pasa a False
        landingFocus.setAttribute('data-focus', 'false');
        iconElement.innerText = 'flip_to_front';
        dataTooltip.setAttribute('data-tooltip', 'Traer el frente');
        pywebview.api.focus_landing_off();
    }
}

function generateScript() {
    pywebview.api.generate_script('py');
}
function generateEvidence() {
    pywebview.api.generate_script('doc');
}

function captureScreen() {
    pywebview.api.capture_screen();
}

function deleteAllSteps(){
    pywebview.api.reset_recorder_steps();
}

function deleteCardStep(index) {
    pywebview.api.delete_card_step(index);
}

function reoderCardsIndexs(reorderEventsRecordedList){
    pywebview.api.reorder_card_index(reorderEventsRecordedList);
}