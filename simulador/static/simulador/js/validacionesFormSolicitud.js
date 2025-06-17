// funcion para validar el formulario
export function validarFormulario(formData){
    let esValido = true // al comienzo siempre va a ser valido
    let edad = null // guardamos la edad para una validacion en antiguedad laboral

    // recorre cada input del formulario y realiza las validaciones con sus metodos
    for(let [llave, valor] of formData.entries()){
        const input = document.getElementById(llave)

        if (!input) {
            continue
        }

        input.addEventListener('focus', ()=>{
            input.classList.remove("input_error")
            eliminarErrorInput(input)
        })

        valor = valor.trim()
        if(!valor){
            textoErrorInput(input, "El campo esta vacio")
            esValido = false
        }
        else if (llave === "nombreCompleto"){
            if(!validarInputNombre(input, valor)) esValido = false
        }
        else if (llave === "edad"){
            const valorNumerico = parseInt(valor, 10)
            if (!isNaN(valorNumerico)) edad = valorNumerico //guardo la edad para pasarsela a la validacion de antiguedad laboral
            if(!validarInputEdad(input, valor)) esValido = false
        }
        else if (llave === "email"){
            if(!validarInputEmail(input, valor)) esValido = false
        }
        else if (llave === "celular"){
            if(!validarInputCelular(input, valor)) esValido = false
        }
        else if (llave === "tipoEmpleo"){
            if(!validarSelectTipoEmpleo(input, valor))esValido = false
        }
        else if (llave === "antiguedadLaboral"){
           if(!validarInputAntiguedadLaboral(input, valor, edad))esValido = false
        }
        else if (llave === "ingresoBrutoMensual"){
            if(!validarInputIngresoBruto(input, valor))esValido = false
        }
        else if (llave === "valorPropiedad"){
            if(!validarInputValorPropiedad(input, valor))esValido = false
        }
        else if (llave === "ahorrosDisponibles"){
            if(!validarInputAhorrosDisponibles(input, valor))esValido = false
        }
        else if (llave === "plazoFinanciamiento"){
            if(!validarInputPlazoFinanciamiento(input, valor))esValido = false
        }
    }
    return esValido
}

// funcion para aplicar error (span)
function textoErrorInput(input, mensaje) {
    const errorSpan = document.getElementById(`error-${input.id}`)
    if (errorSpan) {
        errorSpan.textContent = mensaje
        errorSpan.style.display = 'block'
        input.classList.add("input_error")
    }
}

// funcion para eliminar error (span)
function eliminarErrorInput(input) {
    const errorSpan = document.getElementById(`error-${input.id}`)
    if (errorSpan) {
        errorSpan.textContent = ''
        errorSpan.style.display = 'none'
        input.classList.remove("input_error")
    }
}

// Validaciones propias para cada campo
// validar input nombre
function validarInputNombre(input, valor){
    const patron = /^[a-záéíóúñ]+(?:\s[a-záéíóúñ]+)*$/i // verifica si es un nombre con solo letras Upper y Lower y espacios
    if(valor.length >= 2 && valor.length <= 100){
        if (!patron.test(valor)){
            textoErrorInput(input, "El nombre es invalido")
            console.log("error")
            return false
        }
    }else{
        textoErrorInput(input, "Nombre: 2 a 100 caracteres")
        return false
    }
    return true
}

// validar input edad
function validarInputEdad(input, valor){
    const valorNumerico = parseInt(valor, 10)
    if (!isNaN(valorNumerico)){
        if(valorNumerico < 18){
            textoErrorInput(input, "La edad minima es 18")
            return false
        }else if (valorNumerico > 100){
            textoErrorInput(input, "La edad maxima es 100")
            return false
        }
    }else{
        textoErrorInput(input, "Edad invalida")
        return false
    }
    return true
}

//validar input email
function validarInputEmail(input, valor){
    const patron = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/ // verifica si es un email valido
    if(valor.length >= 6 && valor.length <= 320){
        if (!patron.test(valor)){
            textoErrorInput(input, "El email es invalido")
            return false
        }
    }else{
        textoErrorInput(input, "Email: 6 a 320 caracteres")
        return false
    }
    return true
}

//validar input celular
function validarInputCelular(input, valor){
    const patron =  /^\+?[0-9]{6,25}$/ // verifica si es un celular valido
    if(valor.length >= 6 && valor.length <= 25){
        if (!patron.test(valor)){
            textoErrorInput(input, "El celular es invalido")
            return false
        }
    }else{
        textoErrorInput(input, "Celular: 6 a 25 caracteres")
        return false
    }
    return true
}

//validar select tipo de empleo
function validarSelectTipoEmpleo(select, valor){
    if (valor && valor !== ""){
        select.classList.remove("input_error")
        return true
    }else{
        select.classList.add("input_error")
        return false
    }
}

// validar input antiguedad laboral
function validarInputAntiguedadLaboral(input, valor, edad){
    const valorNumerico = parseInt(valor, 10)
    if (!isNaN(valorNumerico)){
        if(valorNumerico < 0){
            textoErrorInput(input, "Antiguedad minima: 0")
            return false
        }else if (valorNumerico > 100){
            textoErrorInput(input, "Antiguedad maxima: 100")
            return false
        }else if(valorNumerico >= edad){
            textoErrorInput(input, "La antiguedad no puede ser igual o mayor que la edad")
            return false
        }else if(edad-valorNumerico < 16){
            textoErrorInput(input, "La antiguedad no es valida (Años laborales a partir de 16 años)")
            return false
        }
    }else{
        textoErrorInput(input, "Antiguedad invalida")
        return false
    }
    return true
}

// validar input ingreso bruto mensual
function validarInputIngresoBruto(input, valor){
    const valorNumerico = parseInt(valor, 10)
    if (!isNaN(valorNumerico)){
        if(valorNumerico < 10000){
            textoErrorInput(input, "Ingreso bruto minimo: $10.000")
            return false
        }else if (valorNumerico > 100000000){
            textoErrorInput(input, "Ingreso bruto maximo $100.000.000")
            return false
        }
    }else{
        textoErrorInput(input, "Ingreso bruto invalido")
        return false
    }
    return true
}

// validar input valor de la propiedad
function validarInputValorPropiedad(input, valor){
    const valorNumerico = parseInt(valor, 10)
    if (!isNaN(valorNumerico)){
        if(valorNumerico < 10000){
            textoErrorInput(input, "Valor propiedad minimo: $10.000")
            return false
        }else if (valorNumerico > 1000000000){
            textoErrorInput(input, "Valor propiedad maximo: $1.000.000.000")
            return false
        }
    }else{
        textoErrorInput(input, "Valor de la propiedad invalido")
        return false
    }
   return true
}

// validar input ahoros disponibles
function validarInputAhorrosDisponibles(input, valor){
    const valorNumerico = parseInt(valor, 10)
    if (!isNaN(valorNumerico)){
        if(valorNumerico < 1){
            textoErrorInput(input, "Ahorros minimos: $1")
            return false
        }else if (valorNumerico > 1000000000){
            textoErrorInput(input, "Ahorros maximos: $1.000.000.000")
            return false
        }
    }else{
        textoErrorInput(input, "Ahorros disponibles invalidos")
        return false
    }
    return true
}

// validar input plazo de financiamiento
function validarInputPlazoFinanciamiento(input, valor){
    const valorNumerico = parseInt(valor, 10)
    if(!isNaN(valorNumerico)){
        if(valorNumerico < 1){
            textoErrorInput(input, "Plazo minimo: 1 año")
            return false
        }else if (valorNumerico > 30){
            textoErrorInput(input, "Plazo maximo: 30 años")
            return false
        }
    }else{
        textoErrorInput(input, "Plazo invalido")
        return false
    }
    return true
}

