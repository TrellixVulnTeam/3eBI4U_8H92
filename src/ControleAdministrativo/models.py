from django.db import models

# Create your models here.

class FuncionarioCargo(models.Model):
    
    cargo   =    models.CharField(max_length = 100, null = True, blank = True)

class FuncionarioNivel(models.Model):

    nivel       =   models.CharField(max_length = 100, null = True, blank = True)