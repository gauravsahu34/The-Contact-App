from django.db import models

# Create your models here.
class Message(models.Model):
    name = models.CharField(max_length=250, null=True)
    contact_id = models.IntegerField(null=True)
    text = models.TextField(max_length=400)
    OTP = models.CharField(max_length=250)
    sms_time = models.DateTimeField(null=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return self.name
