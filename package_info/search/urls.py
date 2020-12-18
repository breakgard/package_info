from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result', views.result, name='result'),
    path('load_packages', views.load_packages, name='load_packages'),
    path('schedule_package_load', views.schedule_package_load, name='schedule_package_load'),
    path('api/search_package_info', views.result_json, name='result_json')
]
