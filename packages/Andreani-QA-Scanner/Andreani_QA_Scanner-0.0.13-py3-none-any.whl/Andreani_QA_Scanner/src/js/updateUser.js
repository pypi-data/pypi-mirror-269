let current_window = document.defaultView;


function exitJiraConfigs(){
    pywebview.api.call_exit_jira_configs();
}

function openJiraConfigFolder(){
     pywebview.api.call_open_jira_config_folder();
}

function autofill(datos){
    document.getElementById('jiraId').value = datos['JIRA-ID'];
    document.getElementById('jiraServer').value = datos['JIRA-SERVER'];
    document.getElementById('jiraToken').value = datos['JIRA-TOKEN'];
}

function checkAndSave() {
    // Crear una variable booleana llamada "isValid"
    let jiraIdOk = true;
    let jiraServerOk = true;
    let jiraTokenOk = true;
    // Validación para jiraId
    let jiraId = document.getElementById("jiraId").value;
    if (jiraId.trim() === "" || /[^a-zA-Z0-9]/.test(jiraId)) {
        jiraIdOk = false;
        var toastHTML = '<i class="material-icons right" >error</i><span>El id ingresado no es correcto, intente nuevamente</span>';
        M.toast({html: toastHTML, displayLength:3000, classes: 'rounded'});
    }

    // Validación para jiraServer
    let jiraServer = document.getElementById("jiraServer").value;
    if (jiraServer.trim() === "") {
        jiraServerOk = false;
        var toastHTML = '<i class="material-icons right" >error</i><span>El Jira Host ingresado no es correcto, intente nuevamente</span>';
        M.toast({html: toastHTML, displayLength:3000, classes: 'rounded'});
    }

    // Validación para jiraToken
    let jiraToken = document.getElementById("jiraToken").value;
    if (
        jiraToken.trim() === "" ||
        !/^[a-zA-Z0-9]+$/.test(jiraToken) ||
        jiraToken.length < 0 ||
        jiraToken.length > 6
    ) {
        jiraTokenOk = false;
        var toastHTML = '<i class="material-icons right" >error</i><span>El Token ingresado no es correcto, intente nuevamente</span>';
        M.toast({html: toastHTML, displayLength:3000, classes: 'rounded'});
    }
    if(jiraIdOk && jiraServerOk && jiraTokenOk)
    {
        pywebview.api.call_check_and_save(jiraId, jiraServer, jiraToken);
        var toastHTML = '<i class="material-icons right" >fingerprint</i><span>Los datos fueron actualizazos \n correctamente</span>';
        M.toast({html: toastHTML, displayLength:3000, classes: 'rounded'});
    }
    // LLama a la funcion open_jira_config_window desde la vista.
    // los comandos que llegan a este archivo vienen desde el JiraUserConfig.html

}

function destroyUserWindow(){
    window.self.close();
}

//focus window stuff
function focusWindow(){
    //realiza focus a la ventana User [no funciona]
    pywebview.api.get_ventana(current_window);
}

