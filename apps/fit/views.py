from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def logins(request):
    login_template = 'fit/login.html'
    if request.method == 'GET':
        return login_render(request,login_template)
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST["password"])
        if user is None:
            return login_render(request,login_template,'Usuario y/o password incorrectos.')
        else:
            login(request,user)
            return redirect('dashboard')
    

def login_render(request,template,msg=''):
    return render(request,template,{
        'frmlogin':AuthenticationForm,
        'error': msg
    })

@login_required
def sesionout(request):
    logout(request)
    return redirect('logins')

def register_user(request):
    modal = False
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                    )
                messages.success(request,"Usuario registrado correctamente")
                modal = True
                return redirect('register')
            except:
                messages.warning(request,"El usuario ya existe")
        else:
            messages.warning(request,"Los password no son iguales ")
    return render(request,'fit/registeruser.html',{
        'form': UserCreationForm,
        'modal': modal
    })