from django.urls import path
from . import views

urlpatterns = [
    path('read/<int:id>', views.readNotification, name = 'notification/read'),
    path('create/creator=<int:creator>&receiver_group=<int:receiver_group>&receiver_user=<int:receiver_user>&related_url=<path:related_url>&title=<str:title>&message=<str:message>&next_url=<path:next_url>', views.createNotification, name = 'notification/create')
]