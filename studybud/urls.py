
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    #for routing
    path('', include('base.urls')),

    path('api/', include('base.api.urls'))
]
