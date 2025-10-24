from django.db import models
from django.core.validators import FileExtensionValidator

class Content(models.Model):
    file=models.FileField(upload_to="contents/",validators=[FileExtensionValidator(allowed_extensions=['pdf','txt','docx','md'])])
    topic=models.CharField(max_length=255,null=True,blank=True)
    title=models.CharField(max_length=255,null=True,blank=True)
    grade=models.CharField(max_length=255,null=True,blank=True)

    