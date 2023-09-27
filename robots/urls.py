from robots.views import add_robot, get_excel
from django.urls import path

app_name = "robots"

urlpatterns = [
    path('add_robot/', add_robot, name='add_robot'),
    path('get_excel/', get_excel, name='get_excel')
]
