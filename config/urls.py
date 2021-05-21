from django.contrib import admin
from django.urls import path, include
from diary import views

urlpatterns = [
    path('', views.index, name='index'),  # '/' 에 해당되는 path
    path('admin/', admin.site.urls),
    path('diary/', include('diary.urls')),
    path('common/', include('common.urls')),
    path('rekog/', views.rekog, name='rekog'),
]