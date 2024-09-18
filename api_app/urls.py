from django.urls import path
from . import views


urlpatterns = [
  
    path('Dashboard/<str:username>',  views.Dashboard),
    path('Login',  views.Login),
    path('Get-Target/<str:username>', views.Get_Target),
    path('Set-Target/<str:username>', views.Set_Target),
    path('Get-Data', views.Data),
    path('Corporate-Name', views.CorporateName),
    path('Coporate-Visit-Form', views.CorporateForm),
    path('Sage-Mitra-Form', views.SageMitraForm),
    path('Home-Visit', views.Home_Visit),
    path('Event-Form', views.EventForm),
    path('Admission-Form', views.AdmissonForm),
    path('Ip-Form', views.IpForm),
    path('Forget-password', views.Forget_password),
    path('Reset-password', views.Reset_password),
    path('Site-Visit', views.SiteVisitFrom),
    path('Get-Site-Visit-Data', views.GetClientData),
    path('Get-City-Data', views.CityData),
    # path('Forms-Data/<str:username>/<str:form_id>', views.FormData),
    path('Forms-Data/<str:username>/<str:form_id>', views.FormData),

]  