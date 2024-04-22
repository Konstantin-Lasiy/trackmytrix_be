from django.db import models
from django.conf import settings

class DailyWeight(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='weight_entries')
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    class Meta:
        unique_together = ('user', 'date')
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.weight}"
    