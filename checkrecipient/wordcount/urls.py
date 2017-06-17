from django.conf.urls import url

from wordcount import views

urlpatterns = [
    url(r'^api/upload_emails$', views.upload_emails),
]
