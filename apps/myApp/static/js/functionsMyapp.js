

function eraseErrores(){
    $(".ajax-err").remove();
}  

function renderErrorIn(elId,errores){
    txt = "" 
    i = 0
    for (var error in errores){
        txt += "<li class='error err'>" + errores[error] + "</li>"
        i++
    }
    if (i > 0){
        $("#"+elId).after("<ul class='ajax-err messages'>" + txt + "</ul>")
    }
}  

//DIRECT JAVASCRIPT
function chkErrores(elId) {

    console.log('hola')

    var x = document.getElementById(elId);
    var valor = x.value
    var errores = []
    switch(elId){
        //[via AJAX ]case "email":
        case "title":
            if (valor.length == 0){
                errores.push("Title is required!")
            }
            else if (valor.length <= 3 | valor.length > 100){
                errores.push("Title must be between 4 and 100 characters")
            }
            break;
        case "description":
            if (valor.length == 0){
                errores.push("Description is required!")
            } else if (valor.length <= 10 | valor.length > 200){
                errores.push("Description must be between 11 and 200 characters")
            }
            break;
        case "location":
            if (valor.length == 0){
                errores.push("Location is required!")
            };
    }

    if (errores.length > 0){
        txt = "" 
        i = 0
        for (var error in errores){
            txt += "<li class='error err'>" + errores[error] + "</li>"
            i++
        }
        if (i > 0){
            $("#"+elId).after("<ul class='err_"+elId+"'>" + txt + "</ul>")
        }
    }
    
}

function eraseError(elId){
    $(".err_"+elId).remove();
}  
