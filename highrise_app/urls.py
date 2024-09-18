from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/',  views.EmployeeLogin, name='EmployeeLogin'),
    path('dashboard/', views.EmployeeDashboard, name='EmployeeDashboard'),
    path('corporate-visit/', views.EmployeeCorpoVisit, name='EmployeeCorpoVisit'),
    path('sage-mitra/', views.SageMitra, name='SageMitra'),
    path('logout/', views.Logout, name='Logout'),
    path('event/', views.AccEvent, name='AccEvent'),
    path('set-target/', views.Set_Target, name='Set_Target'),
    path('IP/', views.IP, name='IP'),
    path('Admission/', views.Admission, name='Admission'),
    path('Home-visit/', views.Home_visit, name='Home_visit'),
    path('Forget-Password/', views.Forget_password, name='Forget_password'),
    path('Reset-Password/', views.Reset_password, name='Reset_password'),
    path('Back-Date-Corporate/', views.BackDateCoporate, name='Back_Date_Corp'),
    path('Back-Date-Home/', views.BackDateHome, name='Back_Date_Home'),
    path('Site-Visit/', views.Site_Visit, name='Site_Visit'),
    path('Get-Customer-id/', views.Get_Customer_id, name='Get_Customer_id'),
    path('Get-Cities/', views.Cities, name='Cities'),
    path('Get-Source/', views.SourceData, name='SourceData'),
    path('Get-Home-Data/', views.Get_Home_Data, name='Get_Home_Data'),
   
# 
# ]
]    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)