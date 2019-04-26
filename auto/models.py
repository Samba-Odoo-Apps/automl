from django.db import models
from django.contrib.auth.models import AbstractUser
class UserProfile(AbstractUser):
	phone = models.CharField(max_length=250,null=True,blank=True)

# Create your models here.

class Document(models.Model):
	name = models.CharField(max_length=250, blank=True, null=True)
	data=models.FileField()
	target=models.CharField(max_length=250)
	model=models.FileField(max_length=250, blank=True, null=True)
	scores=models.TextField(blank=True,null=True)

	def __str__(self):
		return self.data.name
class PredictDocument(models.Model):
	name = models.CharField(max_length=250, blank=True, null=True)
	data=models.FileField()
	doc = models.ForeignKey(Document, blank=True, on_delete=models.CASCADE,
		null=True)