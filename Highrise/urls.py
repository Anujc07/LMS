from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
handler404 = 'highrise_admin.views.error_404_view'
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from highrise_app import views

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('app/', include('highrise_app.urls')),
    path('', include('highrise_admin.urls')),
    path('api/', include('api_app.urls')),
    path('Client-Site-Visit/', views.Client_Site_Visit, name='Client_Site_Visit'),
    path('Thank-You/', views.Thank_You, name='Thank_You'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)