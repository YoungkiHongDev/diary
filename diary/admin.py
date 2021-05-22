from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Write)
admin.site.register(Answer)
admin.site.register(Upload)
#upload시 파일명 photo.jpg
#admin 의 password는 123