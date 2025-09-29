from django.urls import path
from ..views import (AdminLoginView, HomeView, AdminDashboardView, RoleDetailView, RoleListCreateView,
                     LocationListCreateView, LocationDetailView, LocationBulkUploadView, RoleCostListCreateView,
                     ReportItemListCreateView, ReportHistoryListCreateView, ReportHistoryDetailView, ReportItemDetailView,
                     CalculateReportView, AvailableRolesView, SendReportView, SendOTPView, PrevReportsView,
                     VerifyOTPView, LeadListCreateView, LeadDetailView, OTPlistView, PendingVerifyOTPView,
                     RoleCostDetailView, PendingSendOTPView, PendingRequestListCreateView, RoleBulkUploadView)

urlpatterns = [
    # Home page (public)
    path('web/home/', HomeView.as_view(), name='home'),

    # Admin Login
    path('web/custom-admin/login/', AdminLoginView.as_view(), name='admin-login'),
    # Admin Dashboard
    path('web/admin/dashboard/', AdminDashboardView.as_view(),
         name='admin-dashboard'),


    # Role Management API
    path('api/v1/roles/', RoleListCreateView.as_view(), name='role-list-create'),
    path('api/v1/roles/<int:pk>/',
         RoleDetailView.as_view(), name='role-detail-view'),
    path('web/roles/upload/', RoleBulkUploadView.as_view(), name='role-upload'),



    # Location Management
    path("api/v1/locations/", LocationListCreateView.as_view(),
         name="location-list-create"),
    path("api/v1/locations/<int:pk>/", LocationDetailView.as_view(),
         name="location-detail-view"),


    path('web/locations/upload/', LocationBulkUploadView.as_view(),
         name='location-bulk-upload'),

    # Role Cost Management
    path("api/v1/rolecosts/", RoleCostListCreateView.as_view(),
         name="rolecost-list-create"),
    path("api/v1/rolecosts/<int:pk>/", RoleCostDetailView.as_view(),
         name="rolecost-detail-view"),


    # lead management
    # for apis
    path('api/v1/leads/', LeadListCreateView.as_view(), name='lead-list-create'),
    path('api/v1/leads/<int:pk>/',
         LeadDetailView.as_view(), name="lead-detail-view"),

    # Report Management
    path("api/v1/reports/", ReportHistoryListCreateView.as_view(),
         name="reporthistory-list-create"),
    path("api/v1/reports/<int:pk>/", ReportHistoryDetailView.as_view(),
         name="reporthistory-detail-view"),

    path("api/v1/reports/<int:report_history_id>/items/",
         ReportItemListCreateView.as_view(), name="reportitem-list-create"),
    path("api/v1/reports/<int:report_history_id>/items/<int:pk>/",
         ReportItemDetailView.as_view(), name="reportitem-detail-view"),


    path('web/reports/send-otp/', SendOTPView.as_view(), name="send-otp"),
    path('web/reports/verify-otp/', VerifyOTPView.as_view(), name="verify-otp"),
    path('web/reports/send-report/', SendReportView.as_view(), name="send-report"),
    path("web/reports/prev-reports/",
         PrevReportsView.as_view(), name="prev-reports"),


    path("web/reports/available-roles/",
         AvailableRolesView.as_view(), name="available-roles"),
    path("web/reports/calculate/", CalculateReportView.as_view(),
         name="calculate-report"),

    path("api/v1/otp/", OTPlistView.as_view(), name="otp-list-view"),


    path("web/pending-request/send-otp/", PendingSendOTPView.as_view(),
         name="pending-request-send-otp"),
    path("web/pending-request/verify-otp/", PendingVerifyOTPView.as_view(),
         name="pending-request-verify-otp"),

    path("web/pending-request/", PendingRequestListCreateView.as_view(),
         name="pending-request-list-create"),

]
