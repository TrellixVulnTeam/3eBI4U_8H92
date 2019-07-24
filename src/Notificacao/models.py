from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.
class Notification(models.Model):

    creator = models.ForeignKey(User, models.CASCADE, 'notification_creator')
    receiver_group = models.ForeignKey(Group, models.CASCADE, 'notification_receiver_group', null = True, blank = True)
    receiver_user = models.ForeignKey(User, models.CASCADE, 'notification_receiver_user', null = True, blank = True)
    related_url = models.URLField(null = True, blank = True)
    title = models.CharField(max_length = 200)
    message = models.CharField(max_length = 500)
    read = models.BooleanField(default = False)


    def clean(self):
        if not self.receiver_group and not self.receiver_user:  # This will check for None or Empty
            raise ValidationError({'receiver_group': _('Even one of receiver_group or receiver_user should have a value.')})
    
    def __str__(self):
        return str(self.title)