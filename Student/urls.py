from django.urls import path

from Student import views

app_name = 'Student'

urlpatterns = [
    path('', views.home, name='home'),
    path('show_data', views.show_data, name='show_data'),
    path('thingspeak_api', views.data_from_thingspeak, name='thingspeak_api'),
    path('fetch_datafrom_thingspeak', views.fetch_datafrom_thingspeak, name='fetch_datafrom_thingspeak'),
    path('live/', views.live_data, name='live_data'),
    path('graph_from_thingspeak', views.graph_from_thingspeak, name='graph_from_thingspeak'),
    path('query', views.query, name='query'),
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('login', views.handeLogin, name="handleLogin"),
    path('logout', views.handelLogout, name="handleLogout"),

]