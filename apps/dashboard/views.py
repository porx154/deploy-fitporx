from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Dashboard
from ..fitprofile.models import FitProfile
from datetime import datetime,date,timedelta
from .forms import PesoForm
# Create your views here.
@login_required
def dashboard(request):
    fecha_actual = datetime.now()
    diccionario_fecha = obtener_rango_fecha()
    data = Dashboard.objects.filter(user=request.user,fit_fcregister__gte=diccionario_fecha['fecha_ini'],fit_fcregister__lte=diccionario_fecha['fecha_fin'])
    return render(request,'dashboard/dashboard.html',{
        'data': data,
        'fecha_actual': fecha_actual.date(),
        'pesos':[
            {
                'pesos_dia':obtener_peso_dia(data)
            }
        ]        
    })
def obtener_peso_dia(data):
    pesos ={
        'Monday':0.0,
        'Tuesday':0.0,
        'Wednesday':0.0,
        'Thursday':0.0,
        'Friday':0.0,
        'Saturday':0.0,
        'Sunday':0.0,
    }
    nomb_dia = ''
    for datos in data:
        nomb_dia = datos.fit_fcregister.strftime('%A')
        pesos[nomb_dia] = datos.fit_weight
    return pesos
    
def obtener_rango_fecha():
    fecha_hoy = date.today()
    nombre_dia = fecha_hoy.strftime('%A')
    fecha_ini = fecha_hoy
    fecha_fin = fecha_ini
    dias_resta = 0
    diccionario_fecha ={}
    match nombre_dia:
        case "Monday":
            dias_resta = 0
        case "Tuesday":
            dias_resta = 1
        case "Wednesday":
            dias_resta = 2
        case "Thursday":
            dias_resta = 3
        case "Friday":
            dias_resta = 4
        case "Saturday":
            dias_resta = 5
        case "Sunday":
            dias_resta = 6
        case _:
            dias_resta = 0
    fecha_ini = fecha_hoy - timedelta(days=dias_resta)
    fecha_fin = fecha_ini + timedelta(days=6)
    diccionario_fecha = {
        'fecha_ini': fecha_ini,
        'fecha_fin': fecha_fin
    }
    return diccionario_fecha
@login_required
def mispesos(request):
    user = request.user
    data = Dashboard.objects.filter(user=user)
    return render(request,'dashboard/consultapesos.html',{
        'consultapesos': data
    })

@login_required
def editpeso(request,id_peso):
    pesos = get_object_or_404(Dashboard,pk=id_peso)
    if request.method == 'GET':
        editform = PesoForm(instance=pesos)
    else:
        editform = PesoForm(request.POST,instance=pesos)
        if editform.is_valid():
            editform.save()
            messages.success(request,"Registro actualizado correctamente")
            return redirect('mispesos')
    return render(request,'dashboard/editpesos.html',{
        'formedit': editform,
        'pesos':pesos
    })

@login_required
def createpeso(request):
    if request.method == 'POST':
        #validacion para que no exista registro de dos pesos en una misma fecha
        frmcreate = PesoForm(request.POST)
        #buscando datos
        dato = Dashboard.objects.filter(user=request.user,fit_fcregister=request.POST['fit_fcregister'])
        if dato:
            messages.info(request,"Ya existe un peso en esta fecha")
            return redirect('createpeso')
        if frmcreate.is_valid():
            dashboard = frmcreate.save(commit=False)#aun no me guarda
            dashboard.user = request.user
            frmcreate.fit_user_crea = request.user.username
            frmcreate.save()
            messages.success(request,"Se creo un nuevo peso")
            return redirect('mispesos')
    else:
        frmcreate = PesoForm()
        
    return render(request,'dashboard/createpeso.html',{
        'frmcreate': frmcreate
    })
def calcula_edad(fecha):
    edad = 0
    year_now = datetime.today()
    edad = year_now.year - fecha.year
    return edad

def calcular_calorias(peso, genero):
    #dato por harry venedict
    CALORIAS_GENERO = {
        'M': 35,
        'F': 33,
    }
    if peso is None or genero not in CALORIAS_GENERO:
        return None
    mantenimiento = peso * CALORIAS_GENERO[genero]
    calorias_extra = mantenimiento * 0.2
    return {
        'mantenimiento': round(mantenimiento),
        'deficit': round(mantenimiento - calorias_extra),
        'superavit': round(mantenimiento + calorias_extra)
    }
def calcular_promedio_semanal(request,peso):
    fc_ini_fin = obtener_rango_fecha()
    users = request.user
    semana = 7
    sumpeso = 0
    if peso is None:
        return None
    dato = Dashboard.objects.filter(user=users,fit_fcregister__gte=fc_ini_fin['fecha_ini'],fit_fcregister__lte=fc_ini_fin['fecha_fin']).aggregate(total=Sum('fit_weight'))
    promedio = round((dato['total'] / semana),2)
    return promedio
@login_required
def conobjetivos(request):
    #obtenemos el perfil
    edad = None
    peso_perdido = 0.0
    calorias = 0.0
    peso_semanal = 0.0
    data_profile = get_object_or_404(FitProfile,user=request.user)
    if data_profile.fit_prof_birth_date:
        edad = calcula_edad(data_profile.fit_prof_birth_date)
    if data_profile.fit_prof_weight:
        calorias = calcular_calorias(data_profile.fit_prof_weight,data_profile.fit_sexo)
        #el peso semana y el peso perdido solo se calculara automaticamente cuando el dia sea domingo
        fecha_hoy = date.today()
        nombre_dia = fecha_hoy.strftime('%A')
        if fecha_hoy == 'Sunday':               
            peso_semanal = calcular_promedio_semanal(request,data_profile.fit_prof_weight)
            peso_perdido = round(data_profile.fit_prof_weight - peso_semanal,2)
    return render(request,'dashboard/objetivos.html',{
        'data_profile': data_profile,
        'edad': edad,
        'calorias': calorias,
        'peso_semanal':peso_semanal,
        'peso_perdido': peso_perdido
    })