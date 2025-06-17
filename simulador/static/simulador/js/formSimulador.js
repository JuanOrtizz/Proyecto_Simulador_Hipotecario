import {generarAlertExito, generarAlertError} from './alertas.js'
import {validarFormulario} from './validacionesFormSolicitud.js'

document.addEventListener('DOMContentLoaded', ()=>{
    // capturo el select para aplicarle un estilo para mejorar UX
    const selectTipoEmpleo = document.getElementById("tipoEmpleo")
    selectTipoEmpleo.addEventListener('change',()=>{
        asignarClaseSelect(selectTipoEmpleo, selectTipoEmpleo.value.trim())
    })

    // capturo el formulario y el token
    const formularioSimulador = document.getElementById("formulario_simulador")
    const csrfToken = document.querySelector('[name = csrfmiddlewaretoken]').value

    // Evento para evitar que se mande el form
    formularioSimulador.addEventListener('submit', (e) =>{
            // evita recargar la pagina al mandar el formulario
            e.preventDefault()
            // captura los datos del formulario
            const formData = new FormData(formularioSimulador)
            // valida los campos
            if(validarFormulario(formData)){
                enviarFormulario(formData, csrfToken, formularioSimulador)
            }
        })
})

// funcion async para utilizar await y manejar asincronia
async function enviarFormulario(formData, csrfToken, formularioSimulador){
    const overlay = document.getElementById("pantalla_carga") // Obtiene el overlay (pantalla de carga)
    overlay.style.display = "flex" // Muestra el overlay (pantalla de carga)
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

            // cargo en el informe del financiamiento los valores.
            document.getElementById("informe_cliente").textContent = data.nombre;
            document.getElementById("informe_importe_solicitado").textContent = `$${data.montoFinalCredito.toLocaleString('es-AR')}*`
            document.getElementById("informe_plazo").textContent = `${data.cantidadCuotas} Cuotas`
            document.getElementById("informe_cuota_mensual").textContent = `$${data.montoCuota.toLocaleString('es-AR')}`

            // vacio el formulario
            formularioSimulador.reset()

            // guardo los id de los spans que tienen la cotizacion en dolar
            const spansDolar = [
                'spanDolarIngresoBrutoMensual',
                'spanDolarValorPropiedad',
                'spanDolarAhorrosDisponibles'
            ]
            // a esos span le aplico un foreach para que por cada id le vacie su contenido al enviar el formulario
            spansDolar.forEach(id => {
                const span = document.getElementById(id)
                if (span) span.textContent = ""
            })

            // scroll hacia el informe
            document.getElementById("contenedor_datos_informe").scrollIntoView({ behavior: "smooth", block: "start" })
            // elimino la clase de forma manual del select para que no parezca que sigue seleccionado al vaciar el formulario
            document.querySelectorAll('.select_seleccionado, .select_no_seleccionado').forEach(el => el.classList.remove('select_seleccionado', 'select_no_seleccionado'))


        }else{
            if(data.errors){
                generarAlertError(data.errors)
            }
            else{
                generarAlertError("Ocurrio un error al enviar la solicitud. Intenta nuevamente")
            }
        }
    }catch(error){
        console.error("Error en la solicitud: ", error)
        generarAlertError("Error al enviar el formulario. Intenta mas tarde")
    }finally {
        overlay.style.display = "none" // oculta el overlay (pantalla de carga)
    }
}

// funcion para asignar una clase al select para que cambie si se eligio un valor o no en el formulario, para mejorar la UX
function asignarClaseSelect(select, valor){
    if(valor && valor !== ""){
        select.classList.add("select_seleccionado")
        select.classList.remove("select_no_seleccionado")
    }else{
        select.classList.add("select_no_seleccionado")
        select.classList.remove("select_seleccionado")
    }
}