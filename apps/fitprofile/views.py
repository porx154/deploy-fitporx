from django.shortcuts import render,get_object_or_404,redirect
from .models import FitProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm,ProfileForm
from django.contrib import messages
# Create your views here.
@login_required
def fitprofiles(request):
    user = request.user
    profile = get_object_or_404(FitProfile,user=request.user)
    if request.method == 'GET':
        frm_user = UserUpdateForm(instance=user)
        frm_profile = ProfileForm(instance=profile)
    else:        
        frm_user = UserUpdateForm(request.POST,instance=user)
        frm_profile = ProfileForm(request.POST,instance=profile)
        telefono = FitProfile.objects.filter(fit_prof_phne=request.POST['fit_prof_phne'])
        if telefono:
            messages.warning(request,"El telefono que intenta registrar ya esta en uso")
            return redirect('fitprofiles')
        if frm_user.is_valid() and frm_profile.is_valid():
            print('request.POST')
            frm_user.save()
            frm_profile.save()
            messages.success(request,'Perfil actualizado corretamente')
            return redirect('fitprofiles')
    
    return render(request,'fitprofile/profile.html',{
        'frmuser': frm_user,
        'frmprofile': frm_profile,
        'genero': frm_profile.fields['fit_sexo'].choices
    })
 
