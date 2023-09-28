from django.db import models

# Create your models here.
class TestModel(models.Model):
    name = models.CharField(max_length=255,default="")
    payload_1 = models.TextField(default="")

    class Meta:
        verbose_name = "Test Model"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super(TestModel, self).save(*args, **kwargs)