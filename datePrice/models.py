from django.db import models

# Create your models here.
class DatePrice(models.Model):
    datetime = models.DateTimeField(null=True);
    price = models.FloatField(null=True)
    
    def __str__(self):
        return str(self.pk)
    
class VirtualModel(models.Model):
    link = models.TextField()
    date_time = models.ForeignKey(DatePrice, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.pk) + " " + str(self.event.event_name)  
    
class OfflineModel(models.Model):
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    place = models.TextField()
    date_time = models.ForeignKey(DatePrice, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.pk) + " " + str(self.event.event_name)  