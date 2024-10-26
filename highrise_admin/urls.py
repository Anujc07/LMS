from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve


urlpatterns = [
    # this is login route
    path('', views.Login, name='Login'),


    # path('admin/create-team/', views.CreateTeam, name='CreateTeam'),
    # path('admin/create-member/', views.CreateMember, name='CreateMember'),


    #this route get dropdown values 
    path('', views.DropDownTeam, name='DropDownTeam'),

    # this is for dashboard route
    path('admin/dashboard/', views.GraphCharts, name='Dashboard'),

    # this is for create new admin for dashboard
    path('admin/sign-in/', views.Sign_in, name='Sign_in'),

    # this 2 route for upload files like enquiry and followup excel file
    path('admin/update-data/', views.UpdateData, name='UpdateData'),
    path('admin/fw-update-data/', views.FollowUploadData, name='FollowUploadData'),

    # logout route
    path('admin/user-logout/', views.UserLogout, name='UserLogout'),
    # path('admin/Lead-Funnel/data/', views.LeadFunnelData, name='LeadFunnelData'),

    # this 2 route for lead funnel section  
    path('admin/Lead-Funnel/', views.LeadFunnel, name='LeadFunnel'),                   
    path('LeadFunnel/Data', views.L_Funnel, name='L_Funnel'),

    # this 2 route for DPR section
    path('admin/Daily-Report/', views.DailyPerReport, name='DailyPerReport'),
    path('DPR/', views.DPR, name='DPR'),

    # this route for leads data section
    path('admin/employee/<str:employee>', views.EmployeeData, name='EmployeeData'),

    # this routes for reports section like team performance, current state funnel and sage mitra, download site visit data
    path('admin/RPT-Team-Performance', views.RPT_team_per, name='RPT_team_per'),
    path('admin/RPT-Funnel', views.RPT_funnel, name='RPT_funnel'),
    path('admin/RPT-SM-Corp', views.RPT_sm_corp, name='RPT_sm_corp'),
    path('admin/', views.SiteVisitData, name='SiteVisitData'),

    # this routes for master section
    path('admin/Delete-Record/', views.Delete_Record, name='Delete_Record'),
    path('admin/Employee-Status/', views.Employee_status, name='Employee_status'),
    path('admin/Corporate-List', views.CorporateEdit, name='CorporateEdit'),
    path('admin/Team-List', views.TeamEdit, name='TeamEdit'),


    # this routes for home visit on dashboard
    path('admin/Home-Visit', views.HomeVisit_By_DGM, name='HomeVisit_By_DGM'),
    path('admin/Corporate-Visit', views.CorpoVisit_By_DGM, name='CorpoVisit_By_DGM'),
    path('admin/corporate-names/<int:selectedTypeId>/', views.get_corporate_names, name='get_corporate_names'),
    
    # this routes for booking form and target assign section
    path('admin/Set-Booking', views.SetBookings, name='SetBookings'),
    path('admin/Target-Assign/', views.Target_assign, name='Target_assign'),

    # this routes for graph section 
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