from django.db import models
from django.contrib.auth.models import User

class Dashboard(models.Model):
    fit_fcregister = models.DateField()
    fit_weight = models.FloatField(default=0.0)
    fit_fccrea = models.DateTimeField(auto_now=True)
    fit_user_crea = models.CharField(max_length=100,null=False)
    fit_fc_modi = models.DateTimeField(auto_now=True)
    fit_user_modi = models.CharField(max_length=100,null=True,blank=True)
    fit_estado = models.BooleanField(default=False)
    user = models.ForeignKey(User,related_name='dashboards',on_delete=models.CASCADE)
    fit_observation = models.TextField(max_length=500, null=True,blank=True,default='')
    class Meta:
        ordering = ['-fit_fccrea']
        
    def __str__(self):
        return super().__str__()