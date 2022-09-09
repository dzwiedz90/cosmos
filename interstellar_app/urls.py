from django.urls import path, re_path

from . import views

app_name = 'interstellar_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='log_out'),
    path('units/', views.units, name='units'),
    path('copyright/', views.copyright, name='copyright'),
    path('interstellar/', views.interstellar_tab, name='interstellar_tab'),
    re_path('^interstellar/detail/(?P<id>\d+)/$', views.interstellar_detail, name='interstellar_detail'),
    path('solar/', views.solar_system_tab, name='solar_tab'),
    re_path('^solar/detail/(?P<id>\d+)/$', views.solar_system_detail, name='solar_system_detail'),
    path('moons/', views.moons_tab, name='moons_tab'),
    re_path('^moons/detail/(?P<id>\d+)/$', views.moons_detail, name='moons_detail'),
    path('favourites/', views.favourites, name='favourites'),
    path('plan/', views.plan, name='plan'),
    path('parse_fav_and_plan/', views.parse_fav_and_plan, name='parse_fav_and_plan'),
    path('delete/', views.delete_fav_or_plan, name='delete_fav_or_plan'),
]
