from django.contrib import admin
from django.urls import path, include
from diary import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),  # '/' 에 해당되는 path
    path('admin/', admin.site.urls),
    path('diary/', include('diary.urls')),
    path('common/', include('common.urls')),
    path('rekog/', views.rekog, name='rekog'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)