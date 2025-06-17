import {validarFormulario} from './validacionesFormContacto.js'
import {generarAlertExito, generarAlertError} from './alertas.js'

document.addEventListener('DOMContentLoaded', ()=>{
    // capturo el formulario y el token
    const formularioContacto = document.getElementById("form_contacto")
    const csrfToken = document.querySelector('[name = csrfmiddlewaretoken]').value

    // Evento para evitar que se mande el form
    formularioContacto.addEventListener('submit', (e) =>{
            // evita recargar la pagina al mandar el formulario
            e.preventDefault()
            // captura los datos del formulario
            const formData = new FormData(formularioContacto)
            // valida los campos
            if(validarFormulario(formData)){
                enviarFormulario(formData, csrfToken, formularioContacto)
            }
        })
})

// funcion async para utilizar await y manejar asincronia
async function enviarFormulario(formData, csrfToken, formularioSimulador){
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
            // genera alerta de exito
            generarAlertExito(data.message)

            // vacio el formulario
            formularioSimulador.reset()

        }else{
            // genera alerta de error
            generarAlertError(data.errors)
        }
    }catch(error){
        console.error("Error en la solicitud: ", error)
        generarAlertError("Error al enviar el formulario. Intenta mas tarde")
    }
}