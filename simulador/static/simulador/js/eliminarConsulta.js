import {generarAlertExito} from './alertas.js'
let consultaIdAEliminar = null // declaro el id de la consulta a eliminar

document.addEventListener('DOMContentLoaded', ()=>{
    const botonesEliminar = document.querySelectorAll('.boton_eliminar') // obtengo todos los botones eliminar de la tabla
    // recorro cada uno de esos botones y les pongo un eventListener
    botonesEliminar.forEach(boton => {
        boton.addEventListener('click', () =>{
            consultaIdAEliminar = boton.getAttribute('data-id') // Obtiene el data-id (Consulta)
            if(consultaIdAEliminar){
                Swal.fire({ // Muestra alerta
                  title: "¿Estas seguro que queres eliminar esta consulta?",
                  text: "No podrás revertir esto",
                  icon: "warning",
                  showCancelButton: true,
                  confirmButtonColor: "#3085d6",
                  cancelButtonColor: "#d33",
                  confirmButtonText: "Si Eliminar",
                  didOpen: () =>{ // agrego esto ya que sino recalcula con esta clase y sube el footer para evitar scroll
                    document.body.classList.remove('swal2-height-auto')
                    document.body.style.overflow = 'auto'
                    document.body.style.paddingRight = '0'
                  }
                }).then((result) => {
                    if (result.isConfirmed) { // si confirma hace un fetch y elimina la consulta con ese id
                        fetch(`/eliminarConsulta/${consultaIdAEliminar}/`,{
                        method: 'GET',
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                        })
                        .then(response => response.json())
                        .then(data =>{
                            const row = document.getElementById(`consulta-${consultaIdAEliminar}`)
                            if(row){
                                row.remove() // elimina de la tabla
                                generarAlertExito("Se ha eliminado con exito.") // muestra alerta
                            }
                        })
                        .catch(error =>{
                            console.error("Error al eliminar:", error)
                        })
                    }
                })
            }
        })
    })
})