from django.db import models
from django.contrib.auth.models import User
class FitProfile(models.Model):
    class Genero(models.TextChoices):
        VACIO = '', 'Selecciones un genero'
        MASCULINO = 'M','Hombre'
        FEMENINO = 'F', 'Mujer'
    
    fit_prof_phne = models.CharField(max_length=20,blank=True,null=True,default='')
    fit_prof_birth_date = models.DateField(null=True,blank=True)
    fit_prof_avatar = models.CharField(max_length=200,blank=True,null=True,default='')
    fit_prof_fc_crea = models.DateTimeField(auto_now_add=True)
    fit_prof_fc_modi = models.DateTimeField(auto_now=True)
    fit_prof_height = models.PositiveBigIntegerField(default=0)
    fit_prof_weight = models.FloatField(default=0.0)
    fit_sexo = models.CharField(max_length=1,choices=Genero.choices,blank=True,null=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='fitprofiles')
    
    class Meta:
        ordering = ['-fit_prof_fc_crea']
        unique_together = ('fit_prof_phne',)
    def __str__(self):
        return super().__str__()
    
  
