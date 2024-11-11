from django.db import models
from django.contrib.auth.models import User


class Tech(models.Model):
    name= models.CharField(max_length=200)
    last_name= models.CharField(max_length=200)
    user = models.OneToOneField(User,on_delete=models.CASCADE,default=1)
    avatar = models.ImageField(null=True, blank=True,upload_to="techs")
    def __str__(self) -> str:
        return f'{self.name} {self.last_name}'