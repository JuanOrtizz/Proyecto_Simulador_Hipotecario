from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from .forms import SolicitudCreditoForm, ContactoForm
from .models import Solicitudes, Consultas
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import SolicitudesSerializer, ConsultasSerializer

#Vista para index(pagina principal)
def pagina_index(request):
    return render(request, 'simulador/index.html')

#Vista para el formulario del simulador de credito hipotecario
def pagina_simulador(request):
    # Variables con valores por defecto para el informe de index
    nombre = None
    montoFinalCredito = None
    cantidadCuotas = None
    montoCuota = None

    if request.method == "POST":
        form = SolicitudCreditoForm(request.POST)
        # verifico si el form es valido
        if form.is_valid():

            #obtengo los datos del formulario
            nombreCompleto = form.cleaned_data["nombreCompleto"]
            edad = form.cleaned_data["edad"]
            email = form.cleaned_data["email"]
            celular = form.cleaned_data["celular"]
            tipoEmpleo = form.cleaned_data["tipoEmpleo"]
            antiguedadLaboral = form.cleaned_data["antiguedadLaboral"]
            ingresoBrutoMensual = form.cleaned_data["ingresoBrutoMensual"]
            valorPropiedad = form.cleaned_data["valorPropiedad"]
            ahorrosDisponibles = form.cleaned_data["ahorrosDisponibles"]
            plazoFinanciamiento = form.cleaned_data["plazoFinanciamiento"]

            # validaciones de los datos
            if tipoEmpleo == "1":
                deducciones = 0.17 #si el tipo de empleo es en relacion de dependencia las deducciones son del 17%
                if antiguedadLaboral < 1:
                    return JsonResponse({"success": False,
                                         "errors":"No calificaste al credito. No tenes la antiguedad laboral minima (1 año)."})
            else:
                deducciones = 0.33 # si el tipo de empleo es independiente (que es el unico otro valor posible) las deducciones son del 33%
                if antiguedadLaboral < 2:
                    return JsonResponse({"success": False,
                                         "errors": "No calificaste al credito. No tenes la antiguedad laboral minima (2 años)."})

            #Calculo el ingreso neto
            deduccionesImporte = ingresoBrutoMensual * deducciones
            ingresoNeto =  ingresoBrutoMensual - deduccionesImporte

            #Calculo el ahorro minimo de la propiedad que es 20%
            ahorroMinimoPropiedad = valorPropiedad * 0.2

            #Si no tiene los ahorros minimos le muestra el mensaje
            if ahorrosDisponibles < ahorroMinimoPropiedad:
                return JsonResponse({"success": False,
                                     "errors": "No calificaste al credito. No tenes los ahorros minimos (20% de la propiedad)."})

            #Calculo el monto solicitado (credito)
            montoSolicitado = valorPropiedad - ahorrosDisponibles

            #Calculo la cantidad de cuotas del credito
            cantidadCuotas = plazoFinanciamiento * 12

            #Calculo el monto de intereses del banco (siempre 6,5%)
            montoInteresBanco = montoSolicitado * 0.065

            #Calculo el monto total del credito con los intereses
            montoFinalCredito = montoSolicitado + montoInteresBanco

            #Calculo la cuota mensual del credito
            montoCuota = montoFinalCredito / cantidadCuotas

            #Calculo el maximo a retener (Siempre 30%)
            maxRetener = ingresoNeto * 0.3

            #Si el monto solicitado al banco es menor a 0 no aplica el credito
            if montoSolicitado < 1:
                return JsonResponse({"success": False,
                                     "errors": f"No se puede solicitar un credito menor a 0. Cambie el valor de la propiedad o los ahorros disponibles. "})
            #Si el monto de la cuota es mayor al maximo a retener le muestra el mensaje
            if montoCuota > maxRetener:
                return JsonResponse({"success": False,
                                     "errors":  f"La cuota mensual (${montoCuota:.2f}) supera el maximo a retener (30% [${maxRetener:.2f}]). Te pediremos que modifiques el plazo de financiamiento"})
            else:
                # Guardo en la base de datos
                solicitud = Solicitudes(nombreCompleto=nombreCompleto, edad=edad, email=email, celular=celular,
                                       tipoEmpleo=tipoEmpleo,
                                       antiguedadLaboral=antiguedadLaboral,
                                       ingresoBrutoMensual=ingresoBrutoMensual, valorPropiedad=valorPropiedad,
                                       ahorrosDisponibles=ahorrosDisponibles, plazoFinanciamiento=plazoFinanciamiento,
                                       montoCredito=montoFinalCredito, montoCuota=montoCuota)
                solicitud.save()
                try:
                    #declaro variables con los valores para el mail
                    asunto = f"Credito Hipotecario. Finanzas Raiz"
                    mensaje = "Si no se visualiza correctamente contacta con nosotros"
                    cuerpoMensajeHtml = f"""
                    <html>
                      <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
                        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                          <h2 style="text-align: center; color: #526522;">Informe del Financiamiento del Préstamo</h2>
                          <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                            <tr><td><strong>Nombre completo:</strong></td><td>{nombreCompleto}</td></tr>
                            <tr><td><strong>Edad:</strong></td><td>{edad} años</td></tr>
                            <tr><td><strong>Antigüedad Laboral:</strong></td><td>{antiguedadLaboral} año(s)</td></tr>
                            <tr><td><strong>Ingreso Bruto:</strong></td><td>${ingresoBrutoMensual:,.2f}</td></tr>
                            <tr><td><strong>Porcentaje de deducciones:</strong></td><td>{deducciones * 100:.2f}%</td></tr>
                            <tr><td><strong>Importe de deducciones:</strong></td><td>${deduccionesImporte:,.2f}</td></tr>
                            <tr><td><strong>Ingreso Neto:</strong></td><td>${ingresoNeto:,.2f}</td></tr>
                            <tr><td><strong>Máximo a retener (30%):</strong></td><td>${maxRetener:,.2f}</td></tr>
                            <tr><td><strong>Valor de la propiedad:</strong></td><td>${valorPropiedad:,.2f}</td></tr>
                            <tr><td><strong>Ahorros disponibles:</strong></td><td>${ahorrosDisponibles:,.2f}</td></tr>
                            <tr><td><strong>Monto solicitado:</strong></td><td>${montoSolicitado:,.2f}</td></tr>
                            <tr><td><strong>Plazo de financiamiento:</strong></td><td>{plazoFinanciamiento} años ({cantidadCuotas} cuotas)</td></tr>
                            <tr><td><strong>Interés bancario (6.5%):</strong></td><td>${montoInteresBanco:,.2f}</td></tr>
                            <tr><td><strong>Monto final del préstamo:</strong></td><td>${montoFinalCredito:,.2f}</td></tr>
                            <tr><td><strong>Valor de la cuota mensual:</strong></td><td>${montoCuota:,.2f}</td></tr>
                            <tr><td colspan="2" style="padding-top: 15px;"><strong>Resultado:</strong> <span style="color: green;">Aprobado</span></td></tr>
                          </table>
                        </div>
                      </body>
                    </html>
                    """
                    destinatario = email
                    #envio el mail
                    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [destinatario], fail_silently=False, html_message=cuerpoMensajeHtml )

                except Exception as e:
                    return JsonResponse({"success": False, "errors": f"Error al enviar correo: {e}"})

                # Devuelve la respuesta con el mensaje y los campos para actualizar el informe del credito debajo del formulario
                return JsonResponse ({"success": True,
                                      "message": "Felicidades, calificaste para el prestamo!\nTe enviamos a tu mail el informe del financiamiento.",
                                        'nombre':nombreCompleto,
                                        'montoFinalCredito':montoFinalCredito,
                                        'cantidadCuotas': cantidadCuotas,
                                        'montoCuota': montoCuota})
    else:
        form = SolicitudCreditoForm()

    return render(request, 'simulador/simulador.html', {'form': form})

#Vista para el formulario de contacto
def pagina_contacto(request):
    if request.method == "POST":  # Si el metodo de respuesta es post
        form = ContactoForm(request.POST)
        if form.is_valid():

            #Obtengo los datos del formulario
            nombre = form.cleaned_data["nombre"]
            email = form.cleaned_data["email"]
            celular = form.cleaned_data["celular"]
            mensaje = form.cleaned_data["mensaje"]

            #guardo la consulta en la DB
            consultas = Consultas(
                nombre = nombre,
                celular = celular,
                email = email,
                mensaje = mensaje
            )
            consultas.save()

            return JsonResponse({"success": True,
                                 "message": f"Recibimos tu mensaje y te estaremos contactando al email {email}"})
        else:
            return JsonResponse({"success": False,
                                 "errors": "Error al mandar la consulta, intenta de nuevo"})
    else:
        form = ContactoForm()
    return render(request, 'simulador/contacto.html', {'form': form})

#vista para el dashboard que necesita que si o si un login
@login_required()
def dashboard (request):
    return render(request, 'simulador/dashboard.html')

#vista para las solicitudes desde dashboard
@login_required()
def pagina_solicitudes (request):
    solicitudes = Solicitudes.objects.all()
    return render(request, 'simulador/solicitudes.html', {'solicitudes': solicitudes})

#vista para las consultas desde dashboard
@login_required()
def pagina_consultas (request):
    consultas = Consultas.objects.all()
    return render(request, 'simulador/consultas.html', {'consultas': consultas})

#Vista para modificar una solicitud
@login_required()
def modificar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitudes, id=solicitud_id) # obtengo la solicitud

    if request.method == 'POST':
        form = SolicitudCreditoForm(request.POST)
        if form.is_valid():
            #obtengo los valores (antiguos) del formulario
            emailAntiguo = solicitud.email
            celularAntiguo = solicitud.celular

            # obtengo los datos del formulario que puede cambiar (actuales)
            solicitud.email = form.cleaned_data["email"]
            solicitud.celular = form.cleaned_data["celular"]

            if solicitud.email == emailAntiguo and solicitud.celular == celularAntiguo:
                return JsonResponse({"success": False, "errors": "No realizaste modificaciones"})
            else:
                # actualizo los valores de la solicitud
                solicitud.save()
            return JsonResponse({"success": True, "message": "Solicitud modificada con exito"})
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

    else:
        #lleno el formulario con los datos actuales de la solicitud
        form = SolicitudCreditoForm(initial={
            'nombreCompleto': solicitud.nombreCompleto,
            'edad': solicitud.edad,
            'email': solicitud.email,
            'celular': solicitud.celular,
            'tipoEmpleo': solicitud.tipoEmpleo,
            'antiguedadLaboral': solicitud.antiguedadLaboral,
            'ingresoBrutoMensual': solicitud.ingresoBrutoMensual,
            'valorPropiedad': solicitud.valorPropiedad,
            'ahorrosDisponibles': solicitud.ahorrosDisponibles,
            'plazoFinanciamiento' : solicitud.plazoFinanciamiento
        })

        #creo un array con los campos del formulario
        campos_readonly = [
            'nombreCompleto',
            'edad',
            'tipoEmpleo',
            'antiguedadLaboral',
            'ingresoBrutoMensual',
            'valorPropiedad',
            'ahorrosDisponibles',
            'plazoFinanciamiento'
        ]

        #for para ponerle a esos campos un atributo readonly para evitar su modificacion
        for campo in campos_readonly:
            form.fields[campo].widget.attrs['readonly'] = True

    return render(request, 'simulador/modificar_solicitud.html', {'form': form})

#vista para eliminar una solicitud
@login_required()
def eliminar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitudes, id = solicitud_id)
    solicitud.delete()
    return JsonResponse({"success": True})

#vista para eliminar una consulta
@login_required()
def eliminar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consultas, id = consulta_id)
    consulta.delete()
    return JsonResponse({"success": True})

#clase para el viewSet de Solicitudes
class SolicitudesViewSet(viewsets.ModelViewSet):
    queryset = Solicitudes.objects.all()
    serializer_class = SolicitudesSerializer
    permission_classes = [IsAuthenticated] #Protejo los endpoint, si no esta logeado desde dashboard no puede acceder, en un futuro se usara JWT

# clase para el viewSet de Consultas
class ConsultasViewSet(viewsets.ModelViewSet):
    queryset =  Consultas.objects.all()
    serializer_class = ConsultasSerializer
    permission_classes = [IsAuthenticated] #Protejo los endpoint, si no esta logeado desde dashboard no puede acceder en un futuro se usara JWT