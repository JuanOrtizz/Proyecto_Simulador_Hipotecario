import {generarAlertError} from './alertas.js'
import {validarFormulario} from './validacionesFormSolicitud.js'

document.addEventListener('DOMContentLoaded', ()=>{

    // capturo el formulario y el token
    const formularioModificarSolicitud = document.getElementById("form_modificar_solicitud")
    const csrfToken = document.querySelector('[name = csrfmiddlewaretoken]').value

    // Evento para evitar que se mande el form
    if(formularioModificarSolicitud){
            formularioModificarSolicitud.addEventListener('submit', (e) =>{
                // evita recargar la pagina al mandar el formulario
                e.preventDefault()
                // captura los datos del formulario
                let formData = new FormData(formularioModificarSolicitud)
                // valida los campos
                if(validarFormulario(formData)){
                    enviarFormulario(formData, csrfToken)
                }
            })
    }

})

// funcion async para utilizar await y manejar asincronia
async function enviarFormulario(formData, csrfToken){
    // hago fetch del formulario
    try
    {
        const response = await fetch("",{
            method:"POST",
            body: formData,
            headers:{
                "X-CSRFToken": csrfToken
            }
        })
        const data = await response.json()
        if(data.success){
            // guarda en el sessionStorage el mensaje de exito para mostrar en solicitudes.html
            sessionStorage.setItem('mensajeExito', data.message)
            window.location.href = "/dashboard/solicitudes/" //redirige a solicitudes.html
        }else{
            if(data.errors){
                generarAlertError(data.errors)
            }
            else{
                generarAlertError("Ocurrio un error al modificar la solicitud. Intenta nuevamente")
            }
        }
    }catch(error){
        console.error("Error en la solicitud: ", error)
        generarAlertError("Error al modificar la solicitud. Intenta mas tarde")
    }
}