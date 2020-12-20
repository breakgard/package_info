from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result', views.result, name='result'),
    path('get_max', views.get_max, name='get_max'),
    path('load_packages', views.load_packages, name='load_packages'),
    path('schedule_package_load', views.schedule_package_load, name='schedule_package_load'),
    path('api/search_package_info', views.search_package_info, name='search_package_info')
]
