from django.urls import path
from django.conf import settings
from . import views 
from django.conf.urls.static import static

app_name = 'users'
urlpatterns = [
    path('dashboard', views.index, name='index'),
    path('', views.loginview, name='loginview'),
    path('login/process', views.process, name='process'),
    path('logout', views.processlogout, name='processlogout'),
    path('add', views.add, name='add'),
    path('processadd', views.processadd, name='processadd'),
    path('userlist', views.userlist, name='userlist'),
    path('<int:profile_id>.userdetail/', views.userdetail, name='userdetail'),
    path('<int:profile_id>.delete/', views.delete, name='delete'),
    path('<int:profile_id>.update/', views.update, name='update'),
    path('<int:profile_id>.processedit/', views.processedit, name='processedit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

