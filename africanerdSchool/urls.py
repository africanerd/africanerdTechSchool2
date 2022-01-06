from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500, handler403, handler400
from schools import views

from django.conf import settings #add this
from django.conf.urls.static import static #add this

handler404 = views.error_404
handler500 = views.error_500
handler403 = views.error_403
handler400 = views.error_400


urlpatterns = [
    path('', views.SchoolIndexView2.as_view(), name='school2'),
    path('schools/', include('schools.urls')),
    path('admin/', admin.site.urls),
]


#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
