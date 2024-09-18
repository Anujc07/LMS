from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve


urlpatterns = [
    path('', views.Login, name='Login'),
    path('admin/create-team/', views.CreateTeam, name='CreateTeam'),
    path('admin/create-member/', views.CreateMember, name='CreateMember'),
    path('', views.DropDownTeam, name='DropDownTeam'),
    path('admin/dashboard/', views.Dashboard, name='Dashboard'),
    path('admin/sign-in/', views.Sign_in, name='Sign_in'),
    path('admin/update-data/', views.UpdateData, name='UpdateData'),
    path('admin/fw-update-data/', views.FollowUploadData, name='FollowUploadData'),
    path('admin/user-logout/', views.UserLogout, name='UserLogout'),
    # path('admin/Lead-Funnel/data/', views.LeadFunnelData, name='LeadFunnelData'),
    path('admin/Lead-Funnel/', views.LeadFunnel, name='LeadFunnel'),                   
    path('admin/Daily-Report/', views.DailyPerReport, name='DailyPerReport'),
    path('admin/employee/<str:employee>', views.EmployeeData, name='EmployeeData'),
    path('LeadFunnel/Data', views.L_Funnel, name='L_Funnel'),
    path('DPR/', views.DPR, name='DPR'),
    path('admin/RPT-Team-Performance', views.RPT_team_per, name='RPT_team_per'),
    path('admin/RPT-Funnel', views.RPT_funnel, name='RPT_funnel'),
    path('admin/RPT-SM-Corp', views.RPT_sm_corp, name='RPT_sm_corp'),
    path('admin/Target-Assign/', views.Target_assign, name='Target_assign'),
    path('admin/Delete-Record/', views.Delete_Record, name='Delete_Record'),
    path('admin/Employee-Status/', views.Employee_status, name='Employee_status'),
    path('admin/', views.SiteVisitData, name='SiteVisitData'),
    path('admin/Corporate-List', views.CorporateEdit, name='CorporateEdit'),
    path('admin/Team-List', views.TeamEdit, name='TeamEdit'),
    path('admin/Graph', views.GraphCharts, name='GraphCharts'), 
    path('admin/Graph-Values', views.GraphChartsVlues, name='GraphChartsVlues'), 
    path('admin/Performance-Graph', views.GraphChartsPerformance, name='GraphChartsPerformance'), 
    # path('admin/Employee-Add', views.Add_employee, name='Add_employee'),
    
]

# Serve media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files in development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# This is only for local development when DEBUG=False
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS[0]}),
    ]