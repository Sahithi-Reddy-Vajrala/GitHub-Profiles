from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


        
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	number_of_followers=models.IntegerField(null=True,blank=True)
	time=models.DateTimeField(auto_now=True)
	
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
class Repository(models.Model):
	userprofile=models.ForeignKey(Profile,on_delete=models.CASCADE)
	reponame=models.CharField(max_length=100)
	stars=models.IntegerField(null=True,blank=True)
	




    
