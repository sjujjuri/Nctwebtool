from django.urls import path

from . import views




urlpatterns = [

    path('', views.index, name="index"),
    path('model', views.getModel, name='model'),
    path('year',  views.get_year, name='year'),
    path('about', views.about, name='about'),
    path('results', views.pass_faults_vechicles, name='details_pass')

]