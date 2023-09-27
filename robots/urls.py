from robots.views import add_robot
from django.urls import path

app_name = "robots"

urlpatterns = [
    path('add_robot/', add_robot),
]
