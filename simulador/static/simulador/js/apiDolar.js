document.addEventListener('DOMContentLoaded', ()=>{
    const inputsCalcularValorDolar= [
        {idInput : 'ingresoBrutoMensual', idSpan : 'spanDolarIngresoBrutoMensual'},
        {idInput: 'valorPropiedad', idSpan : 'spanDolarValorPropiedad'},
        {idInput: 'ahorrosDisponibles', idSpan : 'spanDolarAhorrosDisponibles'},
    ]

    // recorro cada input (campo) que esta en el array para agregarle el valor del dolar
    inputsCalcularValorDolar.forEach(campo =>{
        const input = document.getElementById(campo.idInput)
        const span = document.getElementById(campo.idSpan)

        input.addEventListener('input', ()=>{
            calcularValorDolar(input, span)
        })

    })

})

// funcion para obtener el valor del dolar con un fetch
async function obtenerValorDolar(){
    try
    {
        const response = await fetch('https://dolarapi.com/v1/dolares/oficial')
        const data = await response.json()
        return data.venta // devuelvo el precio de venta del dolar OFICIAL
    }catch(error){
        console.error("Error en la solicitud: ", error)
        return null
    }
}

// funcion para calcular el valor del dolar en pesos
async function calcularValorDolar(input, span){
    const valorEnPesos = parseInt(input.value)
    if (!isNaN(valorEnPesos) && valorEnPesos > 0){
        const precioDolar = await obtenerValorDolar()
        if(precioDolar){
            const valorEnDolar = valorEnPesos / parseFloat(precioDolar.toFixed(2))
            span.textContent = `Este importe equivale a ${valorEnDolar.toFixed(2)} dólares (cotización dólar oficial: $${precioDolar.toFixed(2)})`
        }
    }else{
        span.textContent = ""
    }
}